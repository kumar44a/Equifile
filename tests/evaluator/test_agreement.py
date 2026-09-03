from evaluator.agreement import sentiment_agreement
from models import Report


def _report(tone: str) -> Report:
    return Report(doc_id="D1", highlights=["h1", "h2"], risks=[], tone=tone)


def test_matching_tone_returns_true():
    assert sentiment_agreement(_report("cautious"), "cautious") is True


def test_mismatched_tone_returns_false():
    assert sentiment_agreement(_report("positive"), "cautious") is False


def test_no_gold_label_returns_none():
    assert sentiment_agreement(_report("neutral"), None) is None
