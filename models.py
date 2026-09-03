"""Shared data models used across loaders, chunking, summarizer, scoring, evaluator."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Section = Literal["Business", "Results", "Risk Factors", "Liquidity", "Outlook"]
Tone = Literal["positive", "neutral", "cautious"]


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    section: str
    text: str
    metadata: dict = Field(default_factory=dict)


class RiskItem(BaseModel):
    text: str
    section: str
    citation: str  # e.g. "Risk Factors"


class Report(BaseModel):
    doc_id: str
    highlights: list[str]  # expected length 2
    risks: list[RiskItem]  # expected length 2-3
    tone: Tone


class EvalResult(BaseModel):
    doc_id: str
    groundedness: float
    sentiment_agreement: bool | None = None  # None until gold labels exist (Phase 4)
    coherence_score: float
    errors: list[str] = Field(default_factory=list)
