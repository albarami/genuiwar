"""Tests for PDF parser — happy path, empty, malformed."""

from pathlib import Path
from uuid import uuid4

import pytest

from packages.parsers.base import ParseError
from packages.parsers.pdf_parser import PdfParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=FileType.PDF,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestPdfParser:
    def test_clean_pdf_produces_chunks(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_memo.pdf"
        parser = PdfParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) >= 2
        assert result.warnings == []

    def test_clean_pdf_citation_anchors_have_pages(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_memo.pdf"
        parser = PdfParser()
        result = parser.parse(path, _make_doc(path))

        pages = {c.citation_anchor.page for c in result.chunks}
        assert 1 in pages
        assert 2 in pages

    def test_malformed_file_raises_parse_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "corrupt.pdf"
        bad_file.write_text("not a pdf")

        doc = FileDocument(
            file_id=uuid4(),
            original_filename="corrupt.pdf",
            file_type=FileType.PDF,
            file_size_bytes=9,
            storage_path=str(bad_file),
        )

        parser = PdfParser()
        with pytest.raises(ParseError):
            parser.parse(bad_file, doc)
