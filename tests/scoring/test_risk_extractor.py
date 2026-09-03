from chunking.section_chunker import SectionChunker
from loaders.synthetic_loader import SyntheticLoader
from scoring.risk_extractor import RiskExtractor


def _risk_chunk():
    docs = SyntheticLoader().load("FILING_001")
    chunks = SectionChunker().split(docs)
    return next(c for c in chunks if c.section == "Risk Factors")


def test_extract_returns_at_most_top_n():
    chunk = _risk_chunk()
    result = RiskExtractor().extract(chunk, top_n=2)
    assert len(result) <= 2


def test_extract_returns_nonempty_strings():
    chunk = _risk_chunk()
    result = RiskExtractor().extract(chunk)
    assert all(isinstance(s, str) and s.strip() for s in result)
