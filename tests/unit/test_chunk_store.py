"""Tests for InMemoryChunkRepository — add, get, filter, clear."""

from uuid import uuid4

from packages.schemas.evidence import CitationAnchor, EvidenceChunk
from packages.storage import InMemoryChunkRepository


def _chunk(
    file_id=None, content="test", content_type="text", **anchor_kw
):
    fid = file_id or uuid4()
    return EvidenceChunk(
        file_id=fid,
        content=content,
        content_type=content_type,
        citation_anchor=CitationAnchor(file_id=fid, **anchor_kw),
    )


class TestInMemoryChunkRepository:
    def test_add_and_count(self) -> None:
        repo = InMemoryChunkRepository()
        repo.add_chunks([_chunk(), _chunk()])
        assert repo.count() == 2

    def test_get_all(self) -> None:
        repo = InMemoryChunkRepository()
        repo.add_chunks([_chunk(), _chunk()])
        assert len(repo.get_all()) == 2

    def test_get_by_file(self) -> None:
        repo = InMemoryChunkRepository()
        fid = uuid4()
        repo.add_chunks([_chunk(file_id=fid), _chunk()])
        assert len(repo.get_by_file(fid)) == 1

    def test_get_by_file_empty(self) -> None:
        repo = InMemoryChunkRepository()
        repo.add_chunks([_chunk()])
        assert repo.get_by_file(uuid4()) == []

    def test_clear(self) -> None:
        repo = InMemoryChunkRepository()
        repo.add_chunks([_chunk(), _chunk()])
        repo.clear()
        assert repo.count() == 0
        assert repo.get_all() == []

    def test_multiple_files(self) -> None:
        repo = InMemoryChunkRepository()
        f1, f2 = uuid4(), uuid4()
        repo.add_chunks([
            _chunk(file_id=f1),
            _chunk(file_id=f1),
            _chunk(file_id=f2),
        ])
        assert len(repo.get_by_file(f1)) == 2
        assert len(repo.get_by_file(f2)) == 1
