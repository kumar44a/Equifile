from chunking.section_chunker import SectionChunker
from loaders.synthetic_loader import SyntheticLoader


def test_chunk_count_matches_document_count():
    docs = SyntheticLoader().load("FILING_001")
    chunks = SectionChunker().split(docs)
    assert len(chunks) == len(docs)


def test_chunk_ids_are_unique():
    docs = SyntheticLoader().load("FILING_001")
    chunks = SectionChunker().split(docs)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_metadata_includes_char_len():
    docs = SyntheticLoader().load("FILING_001")
    chunks = SectionChunker().split(docs)
    assert all("char_len" in c.metadata for c in chunks)
    assert all(c.metadata["char_len"] == len(c.text) for c in chunks)
