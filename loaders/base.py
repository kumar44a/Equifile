"""Loader interface — deliberately shaped like LangChain's Document/loader
pattern so a real PyPDFLoader-backed adapter can be swapped in later without
touching chunking, summarization, or evaluation code.

Do not add a hard `langchain` dependency here. Keep this interface dependency-free.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Document:
    """Mimics langchain.schema.Document's shape: page_content + metadata."""

    page_content: str
    metadata: dict = field(default_factory=dict)


class BaseLoader(ABC):
    """All loaders (synthetic, future real-PDF) implement this."""

    @abstractmethod
    def load(self, source: str) -> list[Document]:
        """Load a filing identified by `source` (e.g. a doc_id or file path)
        and return one or more Document objects.
        """
        raise NotImplementedError
