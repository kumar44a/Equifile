"""Builds the Claude prompt from chunks. Kept separate from claude_client.py so
prompt content can be unit tested without any network call.
"""
from __future__ import annotations

from models import Chunk

SYSTEM_INSTRUCTIONS = """You are an equity analyst assistant. Given filing \
sections, produce a concise, factual, section-cited report. Output strictly \
as JSON matching this shape:

{
  "highlights": ["<bullet 1>", "<bullet 2>"],
  "risks": [
    {"text": "<risk bullet>", "section": "<source section name>", "citation": "<section name>"}
  ],
  "tone": "positive" | "neutral" | "cautious"
}

Rules:
- Exactly 2 highlights.
- 2-3 risks, each grounded in a direct phrase from the source chunk and citing its section.
- Tone is exactly one word from the allowed set.
- Do not invent facts not present in the provided chunks.
"""


def build_prompt(chunks: list[Chunk]) -> str:
    sections_text = "\n\n".join(
        f"[{c.section}]\n{c.text}" for c in chunks
    )
    return f"{SYSTEM_INSTRUCTIONS}\n\nFiling sections:\n\n{sections_text}"
