from loaders.synthetic_loader import SyntheticLoader


def test_load_returns_one_document_per_section():
    loader = SyntheticLoader()
    docs = loader.load("FILING_001")
    sections = {d.metadata["section"] for d in docs}
    assert sections == {"Business", "Results", "Risk Factors", "Liquidity", "Outlook"}


def test_load_attaches_doc_id_metadata():
    loader = SyntheticLoader()
    docs = loader.load("FILING_001")
    assert all(d.metadata["doc_id"] == "FILING_001" for d in docs)


def test_load_missing_filing_raises():
    loader = SyntheticLoader()
    try:
        loader.load("DOES_NOT_EXIST")
        assert False, "expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_list_available_doc_ids_includes_sample():
    loader = SyntheticLoader()
    assert "FILING_001" in loader.list_available_doc_ids()
