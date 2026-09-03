"""Lexicon-based tone + uncertainty scoring. Lexicons live in
data/lexicons/*.json so they're versioned and inspectable, not hardcoded here.
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_LEXICON_DIR = Path(__file__).resolve().parent.parent / "data" / "lexicons"


class LexiconScorer:
    def __init__(self, lexicon_dir: Path | str = DEFAULT_LEXICON_DIR):
        lexicon_dir = Path(lexicon_dir)
        self.positive_words = self._load(lexicon_dir / "positive.json")
        self.negative_words = self._load(lexicon_dir / "negative.json")
        self.uncertainty_words = self._load(lexicon_dir / "uncertainty.json")

    @staticmethod
    def _load(path: Path) -> set[str]:
        if not path.exists():
            return set()
        with path.open(encoding="utf-8") as f:
            return {w.lower() for w in json.load(f)}

    def score_tone(self, text: str) -> str:
        words = text.lower().split()
        pos = sum(1 for w in words if w.strip(".,;:") in self.positive_words)
        neg = sum(1 for w in words if w.strip(".,;:") in self.negative_words)
        unc = sum(1 for w in words if w.strip(".,;:") in self.uncertainty_words)

        if unc > max(pos, neg):
            return "cautious"
        if pos > neg:
            return "positive"
        if neg > pos:
            return "cautious"
        return "neutral"

    def uncertainty_score(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        unc = sum(1 for w in words if w.strip(".,;:") in self.uncertainty_words)
        return unc / len(words)
