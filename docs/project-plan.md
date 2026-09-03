# AI-Powered Equity Filings Summarization & Risk Insight Agent
### Project Plan v1 — Spinnaker Analytics Research Project (Due 17 Sep 2026)

---

## 0. Scope Recap (from assignment email)

Build a compact agent that:
1. Loads a filing (synthetic corpus, LangChain-like loader interface)
2. Chunks it into sections (Business, Results, Risk Factors, Liquidity, Outlook)
3. Generates an analyst-style report: **Highlights** (2 bullets), **Risks** (2–3 bullets, grounded + section-cited), **Tone** (1 word)
4. Evaluates output with proxy metrics: groundedness, sentiment agreement, coherence
5. Ships as either a `POST /summarize` API or a notebook runner
6. Must be swappable to real PDFs later (via LangChain `PyPDFLoader`) without touching the pipeline

**Deliverables:** working API/notebook · `evaluation/sample_summary.json` · 1–2 page evaluation note · README + RUNBOOK.

---

## 1. Lesson Carried Over From Previous Project Feedback

The prior project's core critique wasn't code quality — it was **evidence integrity**: README claimed 70 sources/246 chunks/41 tests, but `pipeline_summary.json` showed 3 docs/5 chunks, and the log stopped mid-run. Numbers didn't reconcile because they were **hand-typed in separate places**.

This plan treats that as a first-class design constraint, not an afterthought — see §6 ("Docs-Sync Guarantee").

Other carried-over good practices: modular single-responsibility files, tests across every pipeline stage, an executed/notebook-with-outputs-preserved submission, and honest documentation of limitations.

---

## 2. High-Level Design (HLD)

```
                    ┌─────────────────────────────────────────────┐
                    │              data/synthetic_filings/          │
                    │   (JSON/text filings: Business, Results,       │
                    │    Risk Factors, Liquidity, Outlook)            │
                    └───────────────────┬───────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────┐
                        │   Loader (LangChain-like)   │◄── swap point:
                        │  SyntheticLoader / PyPDF-    │    real PDFs later
                        │  LoaderAdapter (future)      │
                        └─────────────┬───────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │        Section Chunker      │
                        │ (splits by section, attaches │
                        │  doc_id/section/offsets)      │
                        └─────────────┬───────────────┘
                                      ▼
                ┌─────────────────────┴──────────────────────┐
                ▼                                             ▼
    ┌───────────────────────┐                  ┌───────────────────────────┐
    │  Summarizer (Claude)    │                  │ Lexicon Sentiment/Risk      │
    │  Highlights + citations │                  │ Scorer (tone + uncertainty) │
    └────────────┬────────────┘                  └─────────────┬──────────────┘
                 └───────────────────┬───────────────────────────┘
                                     ▼
                        ┌───────────────────────────┐
                        │      Report Assembler       │
                        │ (Highlights/Risks/Tone JSON) │
                        └─────────────┬───────────────┘
                                      ▼
                ┌─────────────────────┴──────────────────────┐
                ▼                                             ▼
    ┌───────────────────────┐                  ┌───────────────────────────┐
    │  Notebook Runner (CLI-   │              │        Evaluator            │
    │  friendly, per-filing)  │                  │ groundedness / sentiment    │
    └───────────────────────┘                  │ agreement / coherence proxy  │
                                                └─────────────┬──────────────┘
                                                              ▼
                                                evaluation/sample_summary.json
                                                evaluation/eval_note.md
```

**Key design decision:** keep the loader/chunker interface *identical* whether the backend is synthetic data or real PDFs — this is the "swap later" requirement. Implement it as a small abstract interface, not a full LangChain dependency (see §4 rationale).

**Deliverable format decision:** the assignment offers "Working API (POST /summarize) **or** a notebook runner for local tests" — going with the **notebook runner**, since that's the interpretation of the brief's intent. The pipeline logic still lives in plain, importable Python modules (§3.2) so the notebook is a thin orchestration layer over tested code, not where the logic lives. This also means we can drop FastAPI/TestClient from the stack — one less dependency, one less cross-platform surface to worry about.

---

## 3. Low-Level Design (LLD)

### 3.1 Data models (`app/models.py`, pydantic)
```python
class Document(BaseModel):      # mimics langchain.schema.Document
    page_content: str
    metadata: dict               # {doc_id, section, source, char_start, char_end}

class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    section: str                 # Business | Results | RiskFactors | Liquidity | Outlook
    text: str
    metadata: dict

class RiskItem(BaseModel):
    text: str
    section: str
    citation: str                 # e.g. "Risk Factors, para 3"

class Report(BaseModel):
    doc_id: str
    highlights: list[str]         # exactly 2
    risks: list[RiskItem]         # 2-3
    tone: Literal["positive","neutral","cautious"]

class EvalResult(BaseModel):
    doc_id: str
    groundedness: float
    sentiment_agreement: bool
    coherence_score: float
    errors: list[str]
```

### 3.2 Module breakdown
| Module | Responsibility |
|---|---|
| `loaders/base.py` | `BaseLoader` interface — `.load(source) -> list[Document]` |
| `loaders/synthetic_loader.py` | Reads `data/synthetic_filings/*.json`, mimics loader output |
| `loaders/pdf_loader_adapter.py` | Stub wrapping `langchain_community.PyPDFLoader` (Phase 5, not wired in by default) |
| `chunking/section_chunker.py` | Splits `Document` → `list[Chunk]`, attaches section + offsets |
| `summarizer/prompt_builder.py` | Builds Claude prompt from chunks (with strict output schema instructions) |
| `summarizer/claude_client.py` | Thin wrapper over Anthropic SDK; **has a deterministic mock mode** for offline/CI tests |
| `scoring/lexicon_scorer.py` | Lexicon-based tone + uncertainty scoring; lexicons stored as versioned JSON in `data/lexicons/` |
| `scoring/risk_extractor.py` | Pulls risk-heavy snippets from Risk Factors chunks |
| `evaluator/groundedness.py` | Substring-coverage proxy: % of summary claims traceable to source text |
| `evaluator/agreement.py` | Compares predicted tone vs gold label |
| `evaluator/coherence.py` | Bullet-count/length sanity checks |
| `scripts/run_pipeline.py` | Callable pipeline entrypoint — `run(doc_id) -> (Report, EvalResult)` — imported by both the notebook and tests |
| `notebooks/demo_runner.ipynb` | The actual deliverable: walks through loading a synthetic filing, running the pipeline, and displaying the report + eval metrics per filing. Submitted **with all cells executed and outputs preserved** (direct fix for the "rerun to verify" complaint in the previous feedback). |
| `scripts/check_docs_sync.py` | **New** — see §6 |

### 3.3 Notebook contract
The notebook imports `scripts/run_pipeline.run(doc_id)` — no logic lives in notebook cells themselves, only calls + display. This keeps the pipeline unit-testable independent of the notebook, and means the notebook can't silently drift from the tested code path.
```python
from scripts.run_pipeline import run
report, eval_result = run(doc_id="FILING_003")
```

### 3.4 Config
`.env` / `config.yaml` toggles: `LOADER_MODE=synthetic|pdf`, `CLAUDE_MODEL`, `MOCK_LLM=true|false` (mock mode required so tests don't burn API calls or need a key).

---

## 4. Tech Stack (with rationale)

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Matches the LangChain/ML ecosystem expected by the brief |
| Runner | Jupyter notebook over a plain-Python pipeline module | Matches the chosen deliverable (notebook runner); logic stays testable outside the notebook |
| Schemas | Pydantic v2 | Same models double as validation + eval report structures |
| LLM | Anthropic Python SDK (Claude) | Direct requirement (Claude API); use a small, cheap model for this task |
| Loader interface | Custom minimal `BaseLoader` (LangChain-*like*, not a hard LangChain dependency) | Brief says "LangChain-like" — a full LangChain install adds heavy, sometimes version-fragile deps for a feature we use in name only. Keep `langchain-community` as an *optional* extra, imported lazily only inside `pdf_loader_adapter.py` for Phase 5's real-PDF swap. Avoids the native-dependency pain that hurt cross-platform installs in the previous FAISS/sentence-transformers project. |
| Sentiment/tone | Hand-rolled lexicon scorer | Matches brief exactly ("lexicon-based tone+uncertainty scorer"); no ML model needed |
| Testing | pytest + pytest-cov + FastAPI TestClient | Standard, cross-platform, no native deps |
| Lint/format | ruff + black (via pre-commit) | Fast, consistent across Mac/Windows |
| CI | GitHub Actions, matrix: ubuntu / macos / windows | Catches OS-specific breakage before submission, and mechanically enforces §6 |
| Docs | Markdown (README.md, RUNBOOK.md) generated partly from a stats script (§6) | Prevents drift |

**Deliberately excluded:** FAISS, sentence-transformers, SQLite indexing — not required by this brief (that was the *other* project). Keeping the dependency surface small is itself a cross-platform reliability decision.

---

## 5. Testing Strategy

| Level | What | Notes |
|---|---|---|
| Unit | loader (`Document` shape/metadata correctness), chunker (chunk sizes, section boundaries), lexicon scorer (known word lists → known scores), evaluator functions (groundedness/coherence math) | Fully deterministic, zero network calls |
| Integration | Full pipeline via `scripts/run_pipeline.run()`: synthetic filing → `Report` | Runs with `MOCK_LLM=true` so it's fast/free and CI-safe; a separate marked test (`@pytest.mark.live_llm`, skipped by default) hits the real Claude API. This is also what the notebook calls, so passing this test = notebook will behave correctly. |
| Notebook | Manual check that all cells execute top-to-bottom cleanly (`jupyter nbconvert --execute`) before submission | Guards against the "notebook wasn't actually run end-to-end" failure mode |
| Golden/gold-label | Small hand-labeled set of synthetic filings with known tone + expected risk snippets — **authored in Phase 4**, alongside the evaluation work rather than upfront | Used to compute the sentiment-agreement metric the brief requires |
| Docs-sync check | `scripts/check_docs_sync.py` run as a test | See §6 — this is the direct fix for the previous project's flagged issue |
| Coverage | `pytest-cov`, target ≥80% on `loaders/`, `chunking/`, `scoring/`, `evaluator/` | LLM-calling code excluded from the % (mocked in tests, not meaningfully "covered" by assertions on generated text) |

Note: since the deliverable is notebook-based rather than an API, "integration testing" doubles as the notebook's correctness guarantee — see the Notebook row above.

CI runs the full suite on **ubuntu-latest, macos-latest, windows-latest** on every push — this is also the cross-platform compatibility gate, not just a testing nicety.

---

## 6. Docs-Sync Guarantee (fix for the recurring problem)

Root cause last time: numbers in README were typed by hand and drifted from what the run actually produced.

**Fix — make the numbers generated, not typed:**
1. `scripts/check_docs_sync.py`:
   - Counts synthetic filings in `data/synthetic_filings/`
   - Counts chunks produced by a clean pipeline run
   - Counts passing tests via `pytest --collect-only -q`
   - Reads `evaluation/sample_summary.json` entry count
   - Parses a `<!-- STATS -->...<!-- /STATS -->` block in README.md and diffs the numbers there against the above
2. This script runs as a pytest test (`test_docs_sync.py`) — **CI fails if README and reality disagree**, regardless of whether the last edit was made from VS Code on the Mac or Claude Code on mobile.
3. README's stats block is regenerated by the script (`--write` mode) instead of hand-edited, right before each submission/commit.

This makes "README matches the actual submitted evidence" a build-verified fact, not a promise.

---

## 7. Mac / Windows Compatibility

- All file paths via `pathlib.Path` — never hardcoded `/` or `\`.
- `.gitattributes` with `* text=auto eol=lf` to normalize line endings across Mac and Windows checkouts.
- All file I/O opens with explicit `encoding="utf-8"` (Windows defaults to cp1252 otherwise — a classic silent-corruption source).
- No native/compiled dependencies (see §4) — `pip install` should work identically on both OSes without a C/C++ toolchain.
- RUNBOOK.md gives **both** a bash block (Mac) and a PowerShell block (Windows) for every setup/run command — no single-shell-only script.
- Virtual env instructions for both `python -m venv` flows.

---

## 8. Dev Workflow — VS Code (Mac) + Claude Code (mobile), kept in sync

- **Single source of truth:** one GitHub repo. Both environments work only through `git pull` / `git push` — no local-only state.
- Small, frequent commits; push before switching devices, pull before starting a session on either.
- A repo-root `CLAUDE.md` (or `AGENTS.md`) with project conventions (module layout, "never hand-edit the README stats block," test-before-commit) so any Claude instance — desktop or mobile — behaves consistently.
- GitHub Actions CI (§5/§6) is the actual enforcement mechanism: it doesn't matter which client made a change, the pipeline catches drift and cross-platform breakage the same way either way.
- Suggest branch-per-phase (Phase 1–5 from the brief) merged into `main` once each phase's tests + docs-sync check pass.

---

## 9. Milestone Mapping to Brief's Phases

| Phase | Plan section it maps to |
|---|---|
| 1 — Setup & Exploration | §3.2 loaders + chunker, §7 environment setup |
| 2 — Summarization | §3.2 summarizer, §3.3 API contract |
| 3 — Sentiment & Risk Agent | §3.2 lexicon scorer + risk extractor |
| 4 — Evaluation | §3.2 evaluator/*, §5 testing strategy |
| 5 — Polish & Handoff | §6 docs-sync, README/RUNBOOK, optional demo video |

---

## Decisions Locked

1. **Deliverable:** notebook runner (not API) — pipeline logic lives in plain Python modules; notebook is a thin, fully-executed orchestration layer.
2. **Gold-label tone set:** authored in Phase 4, alongside the evaluation work, not upfront.

## Still Open

1. **Claude model choice** for the summarizer (cost/speed vs quality) — worth checking current model options when we get to Phase 2.
