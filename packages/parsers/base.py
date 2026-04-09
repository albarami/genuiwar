"""Parser contract: base class, result model, and error type."""

from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel, Field

from packages.schemas.document import FileDocument
from packages.schemas.evidence import EvidenceChunk


class ParseError(Exception):
    """Raised when a parser encounters an unrecoverable problem."""

    def __init__(self, file_path: str, reason: str) -> None:
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Parse failed for {file_path}: {reason}")


class ParseResult(BaseModel):
    """Output of a successful parse operation."""

    chunks: list[EvidenceChunk] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class BaseParser(ABC):
    """Abstract contract that every file-type parser must implement."""

    @abstractmethod
    def parse(self, file_path: Path, file_doc: FileDocument) -> ParseResult:
        """Parse a file and return normalized evidence chunks with citation anchors.

        Args:
            file_path: Absolute path to the uploaded file on disk.
            file_doc: The FileDocument metadata object for this file.

        Returns:
            ParseResult containing evidence chunks, metadata, and warnings.

        Raises:
            ParseError: If the file cannot be parsed at all.
        """
