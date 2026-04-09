"""Tests for PPTX parser — happy path, empty, malformed."""

from pathlib import Path
from uuid import uuid4

import pytest

from packages.parsers.base import ParseError
from packages.parsers.pptx_parser import PptxParser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


def _make_doc(path: Path) -> FileDocument:
    return FileDocument(
        original_filename=path.name,
        file_type=FileType.PPTX,
        file_size_bytes=path.stat().st_size,
        storage_path=str(path),
    )


class TestPptxParser:
    def test_clean_pptx_produces_chunks(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_slides.pptx"
        parser = PptxParser()
        result = parser.parse(path, _make_doc(path))

        assert len(result.chunks) == 3
        assert result.warnings == []

    def test_clean_pptx_citation_anchors_have_slide_numbers(self, fixtures_dir: Path) -> None:
        path = fixtures_dir / "clean_slides.pptx"
        parser = PptxParser()
        result = parser.parse(path, _make_doc(path))

        slides = [c.citation_anchor.page for c in result.chunks]
        assert slides == [1, 2, 3]

    def test_malformed_file_raises_parse_error(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "corrupt.pptx"
        bad_file.write_text("not pptx")

        doc = FileDocument(
            file_id=uuid4(),
            original_filename="corrupt.pptx",
            file_type=FileType.PPTX,
            file_size_bytes=8,
            storage_path=str(bad_file),
        )

        parser = PptxParser()
        with pytest.raises(ParseError):
            parser.parse(bad_file, doc)
