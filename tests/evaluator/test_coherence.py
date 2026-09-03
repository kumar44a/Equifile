from evaluator.coherence import coherence_score
from models import Report, RiskItem


def _valid_report():
    return Report(
        doc_id="D1",
        highlights=["This highlight is long enough to pass.", "So is this second one here."],
        risks=[
            RiskItem(text="This risk bullet is long enough to pass checks.", section="Risk Factors", citation="Risk Factors"),
            RiskItem(text="This second risk bullet is also long enough.", section="Risk Factors", citation="Risk Factors"),
        ],
        tone="neutral",
    )


def test_valid_report_scores_perfect():
    score, errors = coherence_score(_valid_report())
    assert score == 1.0
    assert errors == []


def test_wrong_highlight_count_flags_error():
    report = _valid_report()
    report.highlights = ["only one highlight here, long enough"]
    score, errors = coherence_score(report)
    assert score < 1.0
    assert any("highlights" in e for e in errors)


def test_too_few_risks_flags_error():
    report = _valid_report()
    report.risks = report.risks[:1]
    score, errors = coherence_score(report)
    assert score < 1.0
    assert any("risks" in e for e in errors)
