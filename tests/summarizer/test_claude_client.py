from chunking.section_chunker import SectionChunker
from loaders.synthetic_loader import SyntheticLoader
from models import Report
from summarizer.claude_client import ClaudeClient


def _chunks(doc_id: str):
    docs = SyntheticLoader().load(doc_id)
    return SectionChunker().split(docs)


def test_mock_summarize_returns_report():
    report = ClaudeClient(mock=True).summarize("FILING_001", _chunks("FILING_001"))
    assert isinstance(report, Report)
    assert len(report.highlights) == 2
    assert report.tone in ("positive", "neutral", "cautious")


def test_mock_tone_is_lexicon_derived_not_hardcoded():
    # FILING_002 is written to be lexicon-positive (growth/record/strong/
    # outperformed, minimal risk language) — this pins the mock summarizer to
    # actually deriving tone from content instead of a fixed default.
    report = ClaudeClient(mock=True).summarize("FILING_002", _chunks("FILING_002"))
    assert report.tone == "positive"


def test_mock_risks_come_from_risk_extractor():
    # FILING_002's Risk Factors section has 3 sentences, so the extractor
    # should surface all 3 rather than a single hardcoded snippet.
    chunks = _chunks("FILING_002")
    risk_text = next(c.text for c in chunks if c.section == "Risk Factors")
    report = ClaudeClient(mock=True).summarize("FILING_002", chunks)
    assert 2 <= len(report.risks) <= 3
    for risk in report.risks:
        assert risk.text in risk_text
