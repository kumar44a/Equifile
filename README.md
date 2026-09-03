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
`python scripts/check_docs_sync.py --write` to refresh it. CI fails the build
if these numbers don't match the actual repo state, to prevent the kind of
README/artifact drift flagged in a previous project review.

<!-- STATS -->
- Synthetic filings: 1
- Collected tests: 26
- Sample summaries in evaluation/sample_summary.json: 0
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
