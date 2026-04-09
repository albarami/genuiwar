"""Tests for EvidenceBundle schema and citation anchor preservation."""

from uuid import uuid4

from packages.retrieval.local import LocalKeywordRetriever
from packages.retrieval.store import ChunkStore
from packages.schemas.evidence import CitationAnchor, EvidenceBundle, EvidenceChunk


def _chunk(content, page=None, section=None, sheet_name=None, row_range=None):
    fid = uuid4()
    return EvidenceChunk(
        file_id=fid,
        content=content,
        citation_anchor=CitationAnchor(
            file_id=fid,
            page=page,
            section=section,
            sheet_name=sheet_name,
            row_range=row_range,
        ),
    )


class TestEvidenceBundleSchema:
    def test_bundle_creation(self) -> None:
        bundle = EvidenceBundle(query="test", total_candidates=0)
        assert bundle.bundle_id is not None
        assert bundle.chunks == []
        assert bundle.file_ids == []

    def test_bundle_with_chunks(self) -> None:
        c = _chunk("some content", page=1)
        bundle = EvidenceBundle(
            query="test",
            chunks=[c],
            file_ids=[c.file_id],
            total_candidates=1,
        )
        assert len(bundle.chunks) == 1
        assert bundle.file_ids[0] == c.file_id


class TestCitationPreservation:
    def test_page_anchor_preserved(self) -> None:
        store = ChunkStore()
        c = _chunk("budget report page one", page=3)
        store.add_chunks([c])

        bundle = LocalKeywordRetriever(store).retrieve("budget", top_k=5)
        assert bundle.chunks[0].citation_anchor.page == 3

    def test_section_anchor_preserved(self) -> None:
        store = ChunkStore()
        c = _chunk("workforce summary data", section="Summary")
        store.add_chunks([c])

        bundle = LocalKeywordRetriever(store).retrieve("workforce", top_k=5)
        assert bundle.chunks[0].citation_anchor.section == "Summary"

    def test_sheet_anchor_preserved(self) -> None:
        store = ChunkStore()
        c = _chunk("budget numbers here", sheet_name="Budget", row_range=(1, 50))
        store.add_chunks([c])

        bundle = LocalKeywordRetriever(store).retrieve("budget", top_k=5)
        anchor = bundle.chunks[0].citation_anchor
        assert anchor.sheet_name == "Budget"
        assert anchor.row_range == (1, 50)

    def test_file_ids_populated_from_chunks(self) -> None:
        store = ChunkStore()
        f1, f2 = uuid4(), uuid4()
        store.add_chunks([
            EvidenceChunk(
                file_id=f1,
                content="budget data",
                citation_anchor=CitationAnchor(file_id=f1),
            ),
            EvidenceChunk(
                file_id=f2,
                content="budget summary",
                citation_anchor=CitationAnchor(file_id=f2),
            ),
        ])

        bundle = LocalKeywordRetriever(store).retrieve("budget", top_k=5)
        assert set(bundle.file_ids) == {f1, f2}
