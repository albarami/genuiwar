"""Tests for evidence chunk creation and citation anchor correctness."""

from pathlib import Path

from packages.parsers.csv_parser import CsvParser
from packages.parsers.docx_parser import DocxParser
from packages.parsers.xlsx_parser import XlsxParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path, ft: FileType) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=ft,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestEvidenceChunkIntegrity:
    def test_every_chunk_has_file_id(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_report.docx"
        doc = _make_doc(path, FileType.DOCX)
        result = DocxParser().parse(path, doc)

        for chunk in result.chunks:
            assert chunk.file_id == doc.file_id

    def test_every_chunk_has_non_empty_content(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_report.docx"
        doc = _make_doc(path, FileType.DOCX)
        result = DocxParser().parse(path, doc)

        for chunk in result.chunks:
            assert chunk.content.strip() != ""

    def test_chunk_ids_are_unique(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_budget.xlsx"
        doc = _make_doc(path, FileType.XLSX)
        result = XlsxParser().parse(path, doc)

        ids = [c.chunk_id for c in result.chunks]
        assert len(ids) == len(set(ids))

    def test_citation_anchor_file_id_matches_chunk(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_data.csv"
        doc = _make_doc(path, FileType.CSV)
        result = CsvParser().parse(path, doc)

        for chunk in result.chunks:
            assert chunk.citation_anchor.file_id == chunk.file_id

    def test_table_content_type_for_spreadsheet(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_budget.xlsx"
        doc = _make_doc(path, FileType.XLSX)
        result = XlsxParser().parse(path, doc)

        for chunk in result.chunks:
            assert chunk.content_type == "table"

    def test_text_content_type_for_paragraphs(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_report.docx"
        doc = _make_doc(path, FileType.DOCX)
        result = DocxParser().parse(path, doc)

        text_chunks = [c for c in result.chunks if c.content_type == "text"]
        assert len(text_chunks) > 0
