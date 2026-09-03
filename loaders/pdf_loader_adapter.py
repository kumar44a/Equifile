"""Future real-PDF loader adapter.

NOT wired in by default (LOADER_MODE=synthetic is the default — see .env / config).
This module intentionally imports langchain_community lazily, inside the method,
so the rest of the project has zero LangChain dependency unless this specific
adapter is actually used.

To activate later:
    pip install langchain-community pypdf
    set LOADER_MODE=pdf in .env
"""
from __future__ import annotations

from pathlib import Path

from loaders.base import BaseLoader, Document


class PDFLoaderAdapter(BaseLoader):
    def load(self, source: str) -> list[Document]:
        try:
            from langchain_community.document_loaders import PyPDFLoader
        except ImportError as e:
            raise ImportError(
                "PDFLoaderAdapter requires 'langchain-community' and 'pypdf'. "
                "Install with: pip install langchain-community pypdf"
            ) from e

        path = Path(source)
        lc_loader = PyPDFLoader(str(path))
        lc_docs = lc_loader.load()

        # Adapt LangChain's Document objects to our own Document dataclass so
        # downstream chunking/summarization code never needs to know which
        # loader produced the data.
        return [
            Document(page_content=d.page_content, metadata=dict(d.metadata))
            for d in lc_docs
        ]
