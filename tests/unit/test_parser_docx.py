"""Tests for DOCX parser — happy path, empty, malformed."""

from pathlib import Path
from uuid import uuid4

import pytest

from packages.parsers.base import ParseError
from packages.parsers.docx_parser import DocxParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=FileType.DOCX,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestDocxParser:
    def test_clean_docx_produces_chunks(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_report.docx"
        parser = DocxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) > 0
        assert result.warnings == []

        text_chunks = [c for c in result.chunks if c.content_type == "text"]
        table_chunks = [c for c in result.chunks if c.content_type == "table"]
        assert len(text_chunks) >= 2
        assert len(table_chunks) >= 1

    def test_clean_docx_citation_anchors_have_sections(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_report.docx"
        parser = DocxParser()
        result = parser.parse(path, _make_doc(path))

        for chunk in result.chunks:
            assert chunk.citation_anchor.section is not None

    def test_empty_docx_returns_warning(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "empty.docx"
        parser = DocxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) == 0
        assert any("no content" in w.lower() for w in result.warnings)

    def test_malformed_file_raises_parse_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "corrupt.docx"
        bad_file.write_text("this is not a docx file")

        doc = FileDocument(
            file_id=uuid4(),
            original_filename="corrupt.docx",
            file_type=FileType.DOCX,
            file_size_bytes=len("this is not a docx file"),
            storage_path=str(bad_file),
        )

        parser = DocxParser()
        with pytest.raises(ParseError):
            parser.parse(bad_file, doc)

    def test_messy_docx_schema_variation(
        self, fixtures_dir: Path
    ) -> None:
        """Messy DOCX with no headings still parses without error."""
        path = fixtures_dir / "messy_report.docx"
        parser = DocxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) >= 1
        for chunk in result.chunks:
            assert chunk.citation_anchor.section == "Document Start"
