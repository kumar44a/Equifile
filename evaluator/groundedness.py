"""Groundedness proxy: how much of the generated report is traceable back to
the source text via substring coverage. Deliberately simple (per brief:
'Groundedness proxy (substring coverage of summary in source)').
"""
from __future__ import annotations

from models import Chunk, Report


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def groundedness_score(report: Report, source_chunks: list[Chunk]) -> float:
    """Fraction of risk-item texts that appear (as a substring, after
    normalization) somewhere in the source chunks. Highlights are excluded
    from this proxy since they're expected to be synthesized, not quoted.
    """
    if not report.risks:
        return 0.0

    source_blob = _normalize(" ".join(c.text for c in source_chunks))
    hits = sum(1 for r in report.risks if _normalize(r.text) in source_blob or _normalize(r.text)[:40] in source_blob)
    return hits / len(report.risks)
