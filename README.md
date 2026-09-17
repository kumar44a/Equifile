# AI-Powered Equity Filings Summarization & Risk Insight Agent

A compact agent that loads an equity filing, chunks it by section, generates
an analyst-style report (Highlights, Risks, Tone), and evaluates the output
with proxy metrics (groundedness, sentiment agreement, coherence). Runs
entirely on a synthetic corpus by default, with a swappable loader interface
for real PDFs later (see RUNBOOK.md).

## Quick start

See `RUNBOOK.md` for full setup (Mac and Windows).

```bash
pip install -r requirements.txt
cp .env.example .env
jupyter notebook notebooks/demo_runner.ipynb
```

## Project stats

The block below is **generated**, not hand-written — run
`python scripts/check_docs_sync.py --write` to refresh it, and
`python scripts/check_docs_sync.py` (no flag) to verify it without writing.
This is enforced locally via `tests/scripts/test_docs_sync.py` (part of the
normal `pytest` run) to prevent the kind of README/artifact drift flagged in
a previous project review. A GitHub Actions workflow
(`.github/workflows/ci.yml`) runs the same check plus the full test suite on
an ubuntu/macos/windows matrix on every push; as of this submission it is
configured but not yet verified green on GitHub, due to an Actions billing
hold on the repo owner's account unrelated to this code.

<!-- STATS -->
- Synthetic filings: 3
- Collected tests: 30
- Sample summaries in evaluation/sample_summary.json: 3
<!-- /STATS -->

## Design docs

- `docs/project-plan.md` — architecture (HLD/LLD), tech stack rationale, testing strategy
- `CLAUDE.md` — project conventions for AI-assisted development (VS Code + Claude Code, Mac + mobile)

## Deliverables (per assignment brief)

- `notebooks/demo_runner.ipynb` — the notebook runner (submitted with all cells executed)
- `evaluation/sample_summary.json` — sample outputs
- `evaluation/eval_note.md` — 1-2 page evaluation note
- This README + `RUNBOOK.md`

## Swapping to real PDFs later

Set `LOADER_MODE=pdf` in `.env` and install the optional dependencies listed
in `requirements.txt`. See `loaders/pdf_loader_adapter.py` — no other code
needs to change, since chunking/summarization/evaluation all work against the
same `Document` interface regardless of loader.
