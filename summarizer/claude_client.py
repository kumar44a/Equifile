"""Thin wrapper over the Anthropic SDK. Supports MOCK_LLM=true for tests/CI so
the pipeline is fully testable without an API key or network access.

Env vars (see .env / RUNBOOK.md):
    MOCK_LLM        "true" | "false" (default: "true" — safe default for CI)
    CLAUDE_MODEL    e.g. "claude-sonnet-4-6"
    ANTHROPIC_API_KEY
"""
from __future__ import annotations

import json
import os

from models import Chunk, Report, RiskItem
from summarizer.prompt_builder import build_prompt


def _mock_response(chunks: list[Chunk]) -> dict:
    """Deterministic fake output used in tests and CI. Derives trivially
    from the input chunks so groundedness checks have something real to
    validate against, without calling the API.
    """
    risk_chunk = next((c for c in chunks if c.section == "Risk Factors"), chunks[0])
    business_chunk = next((c for c in chunks if c.section == "Business"), chunks[0])
    snippet = risk_chunk.text[:80].strip()
    return {
        "highlights": [
            f"Mock highlight derived from {business_chunk.section} chunk.",
            f"Mock highlight derived from {business_chunk.doc_id}.",
        ],
        "risks": [
            {"text": snippet, "section": risk_chunk.section, "citation": risk_chunk.section},
        ],
        "tone": "neutral",
    }


class ClaudeClient:
    def __init__(self, model: str | None = None, mock: bool | None = None):
        self.model = model or os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
        self.mock = mock if mock is not None else os.environ.get("MOCK_LLM", "true").lower() == "true"

    def summarize(self, doc_id: str, chunks: list[Chunk]) -> Report:
        if self.mock:
            raw = _mock_response(chunks)
        else:
            raw = self._call_api(chunks)

        return Report(
            doc_id=doc_id,
            highlights=raw["highlights"],
            risks=[RiskItem(**r) for r in raw["risks"]],
            tone=raw["tone"],
        )

    def _call_api(self, chunks: list[Chunk]) -> dict:
        # Imported lazily so the SDK isn't required in mock-only environments/tests.
        import anthropic

        client = anthropic.Anthropic()
        prompt = build_prompt(chunks)
        message = client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in message.content if block.type == "text")
        return json.loads(text)
