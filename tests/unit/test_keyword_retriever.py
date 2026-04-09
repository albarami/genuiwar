"""Tests for LocalKeywordRetriever — scoring, top-k, filters, edge cases."""

from uuid import uuid4

from packages.retrieval.base import RetrievalFilters
from packages.retrieval.local import LocalKeywordRetriever
from packages.retrieval.store import ChunkStore
from packages.schemas.evidence import CitationAnchor, EvidenceChunk


def _chunk(
    content: str,
    file_id=None,
    content_type: str = "text",
    sheet_name: str | None = None,
    section: str | None = None,
    page: int | None = None,
):
    fid = file_id or uuid4()
    return EvidenceChunk(
        file_id=fid,
        content=content,
        content_type=content_type,
        citation_anchor=CitationAnchor(
            file_id=fid,
            sheet_name=sheet_name,
            section=section,
            page=page,
        ),
    )


def _store_with(*chunks: EvidenceChunk) -> ChunkStore:
    store = ChunkStore()
    store.add_chunks(list(chunks))
    return store


class TestKeywordRetriever:
    def test_basic_keyword_match(self) -> None:
        store = _store_with(
            _chunk("budget allocation report"),
            _chunk("workforce headcount data"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("budget", top_k=5)
        assert len(bundle.chunks) == 1
        assert "budget" in bundle.chunks[0].content

    def test_top_k_limits_results(self) -> None:
        store = _store_with(
            _chunk("budget allocation report"),
            _chunk("budget planning overview"),
            _chunk("budget summary final"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("budget", top_k=2)
        assert len(bundle.chunks) == 2

    def test_no_match_returns_empty(self) -> None:
        store = _store_with(_chunk("workforce headcount"))
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("budget", top_k=5)
        assert len(bundle.chunks) == 0
        assert bundle.file_ids == []

    def test_empty_query_returns_empty(self) -> None:
        store = _store_with(_chunk("some content"))
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("", top_k=5)
        assert len(bundle.chunks) == 0

    def test_empty_store_returns_empty(self) -> None:
        store = ChunkStore()
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("anything", top_k=5)
        assert len(bundle.chunks) == 0
        assert bundle.total_candidates == 0

    def test_filter_by_file_id(self) -> None:
        f1, f2 = uuid4(), uuid4()
        store = _store_with(
            _chunk("budget report", file_id=f1),
            _chunk("budget summary", file_id=f2),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve(
            "budget", top_k=5, filters=RetrievalFilters(file_ids=[f1])
        )
        assert len(bundle.chunks) == 1
        assert bundle.chunks[0].file_id == f1

    def test_filter_by_content_type(self) -> None:
        store = _store_with(
            _chunk("budget data", content_type="text"),
            _chunk("budget data", content_type="table"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve(
            "budget",
            top_k=5,
            filters=RetrievalFilters(content_type="table"),
        )
        assert len(bundle.chunks) == 1
        assert bundle.chunks[0].content_type == "table"

    def test_filter_by_sheet_name(self) -> None:
        store = _store_with(
            _chunk("budget Q1", sheet_name="Q1"),
            _chunk("budget Q2", sheet_name="Q2"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve(
            "budget",
            top_k=5,
            filters=RetrievalFilters(sheet_name="Q1"),
        )
        assert len(bundle.chunks) == 1
        assert bundle.chunks[0].citation_anchor.sheet_name == "Q1"

    def test_total_candidates_reflects_filtered_pool(self) -> None:
        f1 = uuid4()
        store = _store_with(
            _chunk("a", file_id=f1),
            _chunk("b", file_id=f1),
            _chunk("c"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve(
            "a", top_k=5, filters=RetrievalFilters(file_ids=[f1])
        )
        assert bundle.total_candidates == 2

    def test_multiple_keyword_scoring(self) -> None:
        store = _store_with(
            _chunk("budget allocation report workforce"),
            _chunk("budget report"),
            _chunk("workforce data"),
        )
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("budget report", top_k=3)
        assert bundle.chunks[0].content == "budget allocation report workforce"

    def test_case_insensitive(self) -> None:
        store = _store_with(_chunk("Budget Allocation REPORT"))
        r = LocalKeywordRetriever(store)
        bundle = r.retrieve("budget report", top_k=5)
        assert len(bundle.chunks) == 1
