from evaluator.groundedness import groundedness_score
from models import Chunk, Report, RiskItem


def _source_chunks():
    return [
        Chunk(
            chunk_id="c1",
            doc_id="D1",
            section="Risk Factors",
            text="Litigation related to a patent dispute is ongoing and its outcome is uncertain.",
        )
    ]


def test_grounded_risk_scores_full():
    report = Report(
        doc_id="D1",
        highlights=["h1", "h2"],
        risks=[RiskItem(text="Litigation related to a patent dispute is ongoing", section="Risk Factors", citation="Risk Factors")],
        tone="cautious",
    )
    assert groundedness_score(report, _source_chunks()) == 1.0


def test_ungrounded_risk_scores_zero():
    report = Report(
        doc_id="D1",
        highlights=["h1", "h2"],
        risks=[RiskItem(text="Completely fabricated risk not in source at all", section="Risk Factors", citation="Risk Factors")],
        tone="cautious",
    )
    assert groundedness_score(report, _source_chunks()) == 0.0


def test_no_risks_scores_zero():
    report = Report(doc_id="D1", highlights=["h1", "h2"], risks=[], tone="neutral")
    assert groundedness_score(report, _source_chunks()) == 0.0
