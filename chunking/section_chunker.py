"""Splits loaded Documents into Chunks. For the synthetic corpus, each Document
already corresponds to one section, so this is mostly a metadata-enrichment step
(chunk_id, offsets) — but it's kept as an explicit stage because real PDFs
(Phase 5 swap) will need genuine splitting within a section.
"""
from __future__ import annotations

from loaders.base import Document
from models import Chunk


class SectionChunker:
    def split(self, documents: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for i, doc in enumerate(documents):
            doc_id = doc.metadata.get("doc_id", "UNKNOWN")
            section = doc.metadata.get("section", "UNKNOWN")
            chunk_id = f"{doc_id}::{section}::{i}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    section=section,
                    text=doc.page_content,
                    metadata={**doc.metadata, "char_len": len(doc.page_content)},
                )
            )
        return chunks
