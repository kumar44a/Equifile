import os

from models import EvalResult, Report
from scripts.run_pipeline import run


def test_run_produces_report_and_eval_result(monkeypatch):
    monkeypatch.setenv("MOCK_LLM", "true")
    report, eval_result = run("FILING_001")
    assert isinstance(report, Report)
    assert isinstance(eval_result, EvalResult)
    assert report.doc_id == "FILING_001"
    assert eval_result.doc_id == "FILING_001"


def test_run_agreement_is_none_without_gold_labels(monkeypatch):
    monkeypatch.setenv("MOCK_LLM", "true")
    _, eval_result = run("FILING_001")
    # Gold labels are Phase 4 work — data/gold_labels.json doesn't exist yet.
    assert eval_result.sentiment_agreement is None
