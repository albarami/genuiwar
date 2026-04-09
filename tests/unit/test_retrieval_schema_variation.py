"""Tests for retrieval across mixed file types and schema variations."""

from pathlib import Path

from packages.parsers.csv_parser import CsvParser
from packages.parsers.docx_parser import DocxParser
from packages.parsers.xlsx_parser import XlsxParser
from packages.retrieval.base import RetrievalFilters
from packages.retrieval.local import LocalKeywordRetriever
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType
from packages.storage import InMemoryChunkRepository


def _make_doc(path: Path, ft: FileType) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=ft,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestMixedFileRetrieval:
    def test_retrieve_across_docx_and_xlsx(
        self, fixtures_dir: Path
    ) -> None:
        store = InMemoryChunkRepository()

        docx_path = fixtures_dir / "clean_report.docx"
        docx_doc = _make_doc(docx_path, FileType.DOCX)
        docx_result = DocxParser().parse(docx_path, docx_doc)
        store.add_chunks(docx_result.chunks)

        xlsx_path = fixtures_dir / "clean_budget.xlsx"
        xlsx_doc = _make_doc(xlsx_path, FileType.XLSX)
        xlsx_result = XlsxParser().parse(xlsx_path, xlsx_doc)
        store.add_chunks(xlsx_result.chunks)

        retriever = LocalKeywordRetriever(store)
        bundle = retriever.retrieve("Headcount", top_k=10)

        assert len(bundle.chunks) >= 1
        file_ids = set(bundle.file_ids)
        assert len(file_ids) >= 1

    def test_retrieve_csv_and_docx_mixed(
        self, fixtures_dir: Path
    ) -> None:
        store = InMemoryChunkRepository()

        csv_path = fixtures_dir / "clean_data.csv"
        csv_doc = _make_doc(csv_path, FileType.CSV)
        csv_result = CsvParser().parse(csv_path, csv_doc)
        store.add_chunks(csv_result.chunks)

        docx_path = fixtures_dir / "clean_report.docx"
        docx_doc = _make_doc(docx_path, FileType.DOCX)
        docx_result = DocxParser().parse(docx_path, docx_doc)
        store.add_chunks(docx_result.chunks)

        retriever = LocalKeywordRetriever(store)
        bundle = retriever.retrieve("report", top_k=10)
        assert len(bundle.chunks) >= 1

    def test_filter_narrows_across_mixed_types(
        self, fixtures_dir: Path
    ) -> None:
        store = InMemoryChunkRepository()

        csv_path = fixtures_dir / "clean_data.csv"
        csv_doc = _make_doc(csv_path, FileType.CSV)
        csv_result = CsvParser().parse(csv_path, csv_doc)
        store.add_chunks(csv_result.chunks)

        xlsx_path = fixtures_dir / "clean_budget.xlsx"
        xlsx_doc = _make_doc(xlsx_path, FileType.XLSX)
        xlsx_result = XlsxParser().parse(xlsx_path, xlsx_doc)
        store.add_chunks(xlsx_result.chunks)

        retriever = LocalKeywordRetriever(store)

        all_bundle = retriever.retrieve("data", top_k=20)
        filtered_bundle = retriever.retrieve(
            "data",
            top_k=20,
            filters=RetrievalFilters(file_ids=[csv_doc.file_id]),
        )

        assert filtered_bundle.total_candidates <= all_bundle.total_candidates
        for chunk in filtered_bundle.chunks:
            assert chunk.file_id == csv_doc.file_id

    def test_messy_file_chunks_retrievable(
        self, fixtures_dir: Path
    ) -> None:
        store = InMemoryChunkRepository()

        path = fixtures_dir / "messy_report.docx"
        doc = _make_doc(path, FileType.DOCX)
        result = DocxParser().parse(path, doc)
        store.add_chunks(result.chunks)

        retriever = LocalKeywordRetriever(store)
        bundle = retriever.retrieve("workforce", top_k=5)
        assert len(bundle.chunks) >= 1

    def test_citation_anchors_differ_by_type(
        self, fixtures_dir: Path
    ) -> None:
        store = InMemoryChunkRepository()

        docx_path = fixtures_dir / "clean_report.docx"
        docx_doc = _make_doc(docx_path, FileType.DOCX)
        docx_result = DocxParser().parse(docx_path, docx_doc)
        store.add_chunks(docx_result.chunks)

        xlsx_path = fixtures_dir / "clean_budget.xlsx"
        xlsx_doc = _make_doc(xlsx_path, FileType.XLSX)
        xlsx_result = XlsxParser().parse(xlsx_path, xlsx_doc)
        store.add_chunks(xlsx_result.chunks)

        for chunk in docx_result.chunks:
            assert chunk.citation_anchor.section is not None

        for chunk in xlsx_result.chunks:
            assert chunk.citation_anchor.sheet_name is not None
