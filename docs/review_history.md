# Review History

Running record of external review feedback received on this project and its
predecessor. Kept verbatim (not paraphrased after the fact) so future work —
on this project or a new one referencing it — can pull real context instead
of a summary that's drifted from what was actually said.

---

## Predecessor project — carried-over lesson

Quoted from `docs/project-plan.md` §1, written before this repo's first
commit, summarizing feedback on the project that came before Equifile:

> The prior project's core critique wasn't code quality — it was **evidence
> integrity**: README claimed 70 sources/246 chunks/41 tests, but
> `pipeline_summary.json` showed 3 docs/5 chunks, and the log stopped
> mid-run. Numbers didn't reconcile because they were **hand-typed in
> separate places**.
>
> Other carried-over good practices: modular single-responsibility files,
> tests across every pipeline stage, an executed/notebook-with-outputs-
> preserved submission, and honest documentation of limitations.

This is the reason `scripts/check_docs_sync.py` and
`tests/scripts/test_docs_sync.py` exist in this project — see
`docs/project-plan.md` §6 for the full design rationale.

---

## Spinnaker Analytics — Equifile submission review (received 2026-09-19)

Feedback on the AI-Powered Equity Filings Summarization & Risk Insight Agent
submission, quoted in full.

### Strengths

- The project has a clear modular structure covering loading, section
  chunking, summarization, risk and tone scoring, and evaluation. This
  makes the pipeline easier to understand, test, and extend.
- Practical implementation is strong. The submitted notebook contains
  executed outputs, the repository includes sample summaries for three
  synthetic filings, and the full automated test suite was independently
  run during this review with all 30 tests passing.
- The synthetic mode is a useful design choice because the complete
  workflow can be demonstrated without requiring an API key. The run
  instructions also clearly explain how to configure and execute the
  project on macOS and Windows.
- The evaluation is more thoughtful than simply reporting successful
  scores. For example, the report explains why the groundedness score of
  1.0 is largely guaranteed in mock mode and openly documents the
  coherence limitation for FILING_003.
- The loader abstraction provides a sensible path toward real filing PDFs
  without requiring major changes to the downstream chunking and
  summarization pipeline.
- Documentation is detailed and practical, including environment setup,
  testing, notebook execution, documentation synchronization, and the
  planned real-PDF configuration.

### Suggestions for Improvement

- The main demonstrated workflow still relies on only three synthetic
  filings. Add several real equity filing PDFs and show end-to-end results
  from them to demonstrate how the system handles realistic filing length,
  formatting, section boundaries, and noisy extracted text.
- The real Claude API path is implemented but the submitted evaluation
  states that it was not actually run. Including at least a small verified
  live-model experiment would make the AI summarization component much
  more convincing.
- Groundedness currently evaluates risk text using verbatim substring
  matching, which makes the perfect score less meaningful when mock risks
  are extracted directly from the source. A stronger evaluation should
  also assess paraphrased claims and factual support.
- Improve handling of short Risk Factors sections. FILING_003 produces
  only one risk and receives a coherence score of 0.75. A controlled
  fallback to relevant Outlook or other sections could provide useful
  additional risks without artificially duplicating information.
- The PDF loader is presented mainly as a future swap. A practical
  demonstration with actual PDF extraction, including screenshots or
  notebook outputs showing the extracted sections and resulting analysis,
  would better establish that this integration works as intended.
- The project openly documents substantial use of Claude-based development
  tooling in CLAUDE.md. Where AI assistance contributed to implementation,
  continue keeping the distinction between AI-assisted development and
  independently verified design decisions, testing, observations, and
  conclusions clear.

### Overall

> This is a well-organized and genuinely executable submission with good
> testing and unusually clear documentation of its current limitations.
> The next major improvement is to validate the same pipeline on real
> filings and real model-generated summaries rather than relying primarily
> on the controlled synthetic and mock environment.

### Retrospective note (not part of the original feedback)

Two of the "Suggestions" items — a live Claude API run, and real PDF
parsing — were left undone not because they were out of scope, but because
the blockers (an API key; sample real filing PDFs) were treated as facts to
route around (defaulting to mock mode, deferring to "Phase 5") rather than
surfaced as direct questions back to the project owner while there was
still time to resolve them before the deadline. Worth checking for
early on the next project — see the assistant's own memory notes on this.
