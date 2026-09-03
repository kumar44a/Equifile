"""Reads synthetic filings from data/synthetic_filings/*.json.

Expected file shape (one JSON file per filing):
{
  "doc_id": "FILING_001",
  "company": "Example Corp",
  "sections": {
    "Business": "...",
    "Results": "...",
    "Risk Factors": "...",
    "Liquidity": "...",
    "Outlook": "..."
  }
}
"""
from __future__ import annotations

import json
from pathlib import Path

from loaders.base import BaseLoader, Document

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "synthetic_filings"


class SyntheticLoader(BaseLoader):
    def __init__(self, data_dir: Path | str = DEFAULT_DATA_DIR):
        self.data_dir = Path(data_dir)

    def load(self, source: str) -> list[Document]:
        """`source` is a doc_id (filename stem), e.g. 'FILING_001'."""
        path = self.data_dir / f"{source}.json"
        if not path.exists():
            raise FileNotFoundError(f"No synthetic filing found for doc_id={source!r} at {path}")

        with path.open(encoding="utf-8") as f:
            raw = json.load(f)

        doc_id = raw["doc_id"]
        company = raw.get("company", "")
        documents: list[Document] = []
        for section, text in raw["sections"].items():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "doc_id": doc_id,
                        "company": company,
                        "section": section,
                        "source": str(path),
                    },
                )
            )
        return documents

    def list_available_doc_ids(self) -> list[str]:
        """Used by scripts/check_docs_sync.py to count synthetic filings."""
        return sorted(p.stem for p in self.data_dir.glob("*.json"))
