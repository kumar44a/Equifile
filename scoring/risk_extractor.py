"""Pulls risk-heavy snippets from Risk Factors chunks, using the uncertainty
lexicon as a simple relevance signal (sentences with more uncertainty/negative
words score higher).
"""
from __future__ import annotations

import re

from models import Chunk
from scoring.lexicon_scorer import LexiconScorer


def _split_sentences(text: str) -> list[str]:
    # Simple splitter; good enough for synthetic corpus. Revisit if real PDFs
    # (Phase 5) produce messier sentence boundaries.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


class RiskExtractor:
    def __init__(self, scorer: LexiconScorer | None = None):
        self.scorer = scorer or LexiconScorer()

    def extract(self, risk_chunk: Chunk, top_n: int = 3) -> list[str]:
        sentences = _split_sentences(risk_chunk.text)
        scored = [(s, self.scorer.uncertainty_score(s)) for s in sentences]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [s for s, _ in scored[:top_n]]
