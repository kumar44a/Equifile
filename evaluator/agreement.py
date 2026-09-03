"""Sentiment agreement vs gold labels. Gold labels are authored in Phase 4
(data/gold_labels.json — doc_id -> tone). Returns None (not False) when no
gold label exists yet, so callers can distinguish "disagreed" from
"not yet evaluated."
"""
from __future__ import annotations

from models import Report


def sentiment_agreement(report: Report, gold_tone: str | None) -> bool | None:
    if gold_tone is None:
        return None
    return report.tone == gold_tone
