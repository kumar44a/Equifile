# AI-Powered Equity Filings Summarization & Risk Insight Agent

Small agent that reads an equity filing, chunks it by section, and writes an analyst-style summary — Highlights, Risks, Tone — then grades its own work with a few proxy metrics (groundedness, sentiment agreement, coherence).

Ships with a synthetic corpus so you can run the whole thing end-to-end without needing real filings or API access to test on day one. If you want to point it at actual PDFs later, there's a loader you can swap in — see RUNBOOK.md.

## Quick start

RUNBOOK.md has the full setup for both Mac and Windows (there were a couple of Windows-specific gotchas with jupyter and env vars, worth reading if you're on that). Short version:

```bash
pip install -r requirements.txt
cp .env.example .env
jupyter notebook notebooks/demo_runner.ipynb
```

## Project stats

These numbers are generated, not typed by hand — that's on purpose. Run:

```bash
python scripts/check_docs_sync.py --write   # regenerate
python scripts/check_docs_sync.py           # just check, no write
```

Honestly the reason this exists is that on an earlier project the README claimed a test count that hadn't been true for weeks, and it got called out in review. So now it's checked automatically — tests/scripts/test_docs_sync.py runs as part of normal pytest, so if this drifts, the test suite fails, not just the README looking stale.

There's also a GitHub Actions workflow (.github/workflows/ci.yml) running the same check plus the full suite across ubuntu/macos/windows on every push. Small disclosure: it's configured but I haven't actually seen it go green on GitHub yet — there's a billing hold on the account that's blocking Actions minutes, unrelated to the code. It does run clean locally on all three OSes as far as I've tested.

<!-- STATS -->
- Synthetic filings: 3
- Collected tests: 30
- Sample summaries in evaluation/sample_summary.json: 3
<!-- /STATS -->

## Design docs
- `docs/project-plan.md` — architecture (HLD/LLD), why this stack over the alternatives, testing approach
- `docs/review_history.md` — external review feedback on this project and its predecessor, kept verbatim
- `CLAUDE.md` — notes on how this was built with AI assistance (VS Code + Claude Code, Mac + mobile), mostly so I remember my own conventions later

## Deliverables (per assignment brief)
- `notebooks/demo_runner.ipynb` — the notebook, submitted with all cells already executed
- `evaluation/sample_summary.json` — sample outputs
- `evaluation/eval_note.md` — the 1–2 page evaluation writeup
- This README + `RUNBOOK.md`

## Swapping to real PDFs later

Set `LOADER_MODE=pdf` in `.env`, install the optional deps in requirements.txt, and you're mostly done — see `loaders/pdf_loader_adapter.py`. Chunking, summarization, and evaluation are all written against a shared Document interface, so none of that code cares where the text actually came from. That was a deliberate call early on, specifically so swapping the data source wouldn't mean rewriting half the pipeline.
