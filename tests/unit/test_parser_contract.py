"""Verify every registered parser implements the BaseParser contract."""

from packages.parsers import registered_types
from packages.parsers.base import BaseParser
from packages.parsers.csv_parser import CsvParser
from packages.parsers.docx_parser import DocxParser
from packages.parsers.pdf_parser import PdfParser
from packages.parsers.pptx_parser import PptxParser
from packages.parsers.registry import get_parser
from packages.parsers.xlsx_parser import XlsxParser
from packages.schemas.enums import FileType

ALL_PARSERS: list[tuple[FileType, type[BaseParser]]] = [
    (FileType.DOCX, DocxParser),
    (FileType.PDF, PdfParser),
    (FileType.PPTX, PptxParser),
    (FileType.XLSX, XlsxParser),
    (FileType.CSV, CsvParser),
]


class TestParserContract:
    def test_all_five_types_registered(self) -> None:
        types = registered_types()
        for ft in FileType:
            assert ft in types, f"No parser registered for {ft}"

    def test_get_parser_returns_correct_type(self) -> None:
        for file_type, expected_cls in ALL_PARSERS:
            parser = get_parser(file_type)
            assert isinstance(parser, expected_cls)

    def test_all_parsers_are_base_parser_subclasses(self) -> None:
        for _, cls in ALL_PARSERS:
            assert issubclass(cls, BaseParser)

    def test_get_parser_raises_for_unknown_type(self) -> None:
        import pytest

        with pytest.raises(ValueError, match="No parser registered"):
            get_parser("nonexistent")  # type: ignore[arg-type]
