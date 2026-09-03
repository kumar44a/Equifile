"""Single pipeline entrypoint. The notebook imports run() and nothing else —
all real logic lives here and in the loaders/chunking/summarizer/scoring/
evaluator packages, so it's fully unit- and integration-testable outside
the notebook.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from chunking.section_chunker import SectionChunker
from evaluator.agreement import sentiment_agreement
from evaluator.coherence import coherence_score
from evaluator.groundedness import groundedness_score
from loaders.synthetic_loader import SyntheticLoader
from models import EvalResult, Report
from summarizer.claude_client import ClaudeClient

GOLD_LABELS_PATH = Path(__file__).resolve().parent.parent / "data" / "gold_labels.json"


def _load_gold_tone(doc_id: str) -> str | None:
    if not GOLD_LABELS_PATH.exists():
        return None  # expected until Phase 4
    with GOLD_LABELS_PATH.open(encoding="utf-8") as f:
        labels = json.load(f)
    return labels.get(doc_id)


def run(doc_id: str, loader_mode: str | None = None) -> tuple[Report, EvalResult]:
    """Run the full pipeline for a single filing and return (Report, EvalResult).

    loader_mode: "synthetic" (default) or "pdf". Falls back to LOADER_MODE env
    var, then "synthetic".
    """
    mode = loader_mode or os.environ.get("LOADER_MODE", "synthetic")

    if mode == "synthetic":
        loader = SyntheticLoader()
    elif mode == "pdf":
        from loaders.pdf_loader_adapter import PDFLoaderAdapter

        loader = PDFLoaderAdapter()
    else:
        raise ValueError(f"Unknown loader_mode: {mode!r}")

    documents = loader.load(doc_id)
    chunks = SectionChunker().split(documents)

    client = ClaudeClient()
    report = client.summarize(doc_id=doc_id, chunks=chunks)

    grounded = groundedness_score(report, chunks)
    coherence, coherence_errors = coherence_score(report)
    gold_tone = _load_gold_tone(doc_id)
    agreement = sentiment_agreement(report, gold_tone)

    eval_result = EvalResult(
        doc_id=doc_id,
        groundedness=grounded,
        sentiment_agreement=agreement,
        coherence_score=coherence,
        errors=coherence_errors,
    )
    return report, eval_result


def run_all(loader_mode: str | None = None) -> list[tuple[Report, EvalResult]]:
    """Runs the pipeline over every synthetic filing. Used to produce
    evaluation/sample_summary.json.
    """
    loader = SyntheticLoader()
    results = []
    for doc_id in loader.list_available_doc_ids():
        results.append(run(doc_id, loader_mode=loader_mode))
    return results
