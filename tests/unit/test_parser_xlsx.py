"""Tests for XLSX parser — happy path, empty, messy (merged cells)."""

from pathlib import Path
from uuid import uuid4

import pytest

from packages.parsers.base import ParseError
from packages.parsers.xlsx_parser import XlsxParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=FileType.XLSX,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestXlsxParser:
    def test_clean_xlsx_produces_chunks(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_budget.xlsx"
        parser = XlsxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) >= 2
        assert result.warnings == []

    def test_clean_xlsx_has_sheet_names_in_metadata(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_budget.xlsx"
        parser = XlsxParser()
        result = parser.parse(path, _make_doc(path))

        assert "sheet_names" in result.metadata
        names = result.metadata["sheet_names"]
        assert isinstance(names, list)
        assert "Headcount" in names
        assert "Budget" in names

    def test_clean_xlsx_citation_anchors_have_sheet_and_rows(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_budget.xlsx"
        parser = XlsxParser()
        result = parser.parse(path, _make_doc(path))

        for chunk in result.chunks:
            assert chunk.citation_anchor.sheet_name is not None
            assert chunk.citation_anchor.row_range is not None

    def test_messy_xlsx_still_parses(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "messy_budget.xlsx"
        parser = XlsxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) >= 1

    def test_empty_xlsx_returns_warning(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "empty.xlsx"
        parser = XlsxParser()
        result = parser.parse(path, _make_doc(path))

        assert any("empty" in w.lower() for w in result.warnings)

    def test_malformed_file_raises_parse_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "corrupt.xlsx"
        bad_file.write_text("not xlsx")

        doc = FileDocument(
            file_id=uuid4(),
            original_filename="corrupt.xlsx",
            file_type=FileType.XLSX,
            file_size_bytes=8,
            storage_path=str(bad_file),
        )

        parser = XlsxParser()
        with pytest.raises(ParseError):
            parser.parse(bad_file, doc)
