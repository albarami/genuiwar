"""Parser registry: maps FileType to the correct parser implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packages.schemas.enums import FileType

if TYPE_CHECKING:
    from packages.parsers.base import BaseParser


_REGISTRY: dict[FileType, type[BaseParser]] = {}


def register_parser(file_type: FileType):  # type: ignore[no-untyped-def]
    """Class decorator that registers a parser for a given file type."""

    def decorator(cls: type[BaseParser]) -> type[BaseParser]:
        _REGISTRY[file_type] = cls
        return cls

    return decorator


def get_parser(file_type: FileType) -> BaseParser:
    """Instantiate and return the parser registered for *file_type*.

    Raises:
        ValueError: If no parser is registered for the given type.
    """
    parser_cls = _REGISTRY.get(file_type)
    if parser_cls is None:
        raise ValueError(f"No parser registered for file type: {file_type}")
    return parser_cls()


def registered_types() -> list[FileType]:
    """Return a list of file types that have registered parsers."""
    return list(_REGISTRY.keys())
