"""Tests for ChunkStore — add, get, filter, clear."""

from uuid import uuid4

from packages.retrieval.store import ChunkStore
from packages.schemas.evidence import CitationAnchor, EvidenceChunk


def _chunk(file_id=None, content="test", content_type="text", **anchor_kw):
    fid = file_id or uuid4()
    return EvidenceChunk(
        file_id=fid,
        content=content,
        content_type=content_type,
        citation_anchor=CitationAnchor(file_id=fid, **anchor_kw),
    )


class TestChunkStore:
    def test_add_and_count(self) -> None:
        store = ChunkStore()
        store.add_chunks([_chunk(), _chunk()])
        assert store.count() == 2

    def test_get_all(self) -> None:
        store = ChunkStore()
        c1, c2 = _chunk(), _chunk()
        store.add_chunks([c1, c2])
        assert len(store.get_all()) == 2

    def test_get_by_file(self) -> None:
        store = ChunkStore()
        fid = uuid4()
        store.add_chunks([_chunk(file_id=fid), _chunk()])
        assert len(store.get_by_file(fid)) == 1

    def test_get_by_file_empty(self) -> None:
        store = ChunkStore()
        store.add_chunks([_chunk()])
        assert store.get_by_file(uuid4()) == []

    def test_clear(self) -> None:
        store = ChunkStore()
        store.add_chunks([_chunk(), _chunk()])
        store.clear()
        assert store.count() == 0
        assert store.get_all() == []

    def test_multiple_files(self) -> None:
        store = ChunkStore()
        f1, f2 = uuid4(), uuid4()
        store.add_chunks([
            _chunk(file_id=f1),
            _chunk(file_id=f1),
            _chunk(file_id=f2),
        ])
        assert len(store.get_by_file(f1)) == 2
        assert len(store.get_by_file(f2)) == 1
