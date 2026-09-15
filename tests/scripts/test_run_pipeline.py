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


def test_run_agreement_uses_gold_labels(monkeypatch):
    monkeypatch.setenv("MOCK_LLM", "true")
    # data/gold_labels.json (Phase 4) now has a label for every synthetic
    # filing, so agreement should resolve to a bool, not None.
    _, eval_result = run("FILING_001")
    assert eval_result.sentiment_agreement in (True, False)


def test_run_agreement_is_none_for_unlabeled_doc_id(monkeypatch, tmp_path):
    monkeypatch.setenv("MOCK_LLM", "true")
    monkeypatch.setattr("scripts.run_pipeline.GOLD_LABELS_PATH", tmp_path / "missing.json")
    _, eval_result = run("FILING_001")
    assert eval_result.sentiment_agreement is None
