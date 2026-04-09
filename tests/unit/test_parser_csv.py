"""Tests for CSV parser — happy path, empty, schema variation."""

from pathlib import Path
from uuid import uuid4

from packages.parsers.csv_parser import CsvParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=FileType.CSV,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestCsvParser:
    def test_clean_csv_produces_chunks(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_data.csv"
        parser = CsvParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) >= 1
        assert result.warnings == []

    def test_clean_csv_has_headers_in_metadata(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_data.csv"
        parser = CsvParser()
        result = parser.parse(path, _make_doc(path))

        assert "headers" in result.metadata
        headers = result.metadata["headers"]
        assert isinstance(headers, list)
        assert "Name" in headers

    def test_clean_csv_citation_anchors_have_row_range(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_data.csv"
        parser = CsvParser()
        result = parser.parse(path, _make_doc(path))

        for chunk in result.chunks:
            assert chunk.citation_anchor.row_range is not None

    def test_empty_csv_returns_warning(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "empty.csv"
        parser = CsvParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) == 0
        assert any("empty" in w.lower() for w in result.warnings)

    def test_different_delimiter(self, tmp_path: Path) -> None:
        tsv = tmp_path / "data.csv"
        tsv.write_text("Col1\tCol2\n1\t2\n3\t4\n", encoding="utf-8")

        doc = FileDocument(
            file_id=uuid4(),
            original_filename="data.csv",
            file_type=FileType.CSV,
            file_size_bytes=tsv.stat().st_size,
            storage_path=str(tsv),
        )

        parser = CsvParser()
        result = parser.parse(tsv, doc)
        assert len(result.chunks) >= 1
