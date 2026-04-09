"""File parsers — type-specific parsing and normalization."""

import packages.parsers.csv_parser as _csv  # noqa: F401 — register on import
import packages.parsers.docx_parser as _docx  # noqa: F401
import packages.parsers.pdf_parser as _pdf  # noqa: F401
import packages.parsers.pptx_parser as _pptx  # noqa: F401
import packages.parsers.xlsx_parser as _xlsx  # noqa: F401
from packages.parsers.base import BaseParser, ParseError, ParseResult
from packages.parsers.registry import get_parser, register_parser, registered_types

__all__ = [
    "BaseParser",
    "ParseError",
    "ParseResult",
    "get_parser",
    "register_parser",
    "registered_types",
]
