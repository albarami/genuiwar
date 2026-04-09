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
    """Output of a successful parse operation.

    Contains both the normalized document object (with page_count,
    sheet_names, detected_schema populated by the parser) and the
    extracted evidence chunks.
    """

    document: FileDocument
    chunks: list[EvidenceChunk] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class BaseParser(ABC):
    """Abstract contract that every file-type parser must implement.

    Each parser receives a FileDocument with basic upload metadata already set
    (file_id, filename, type, size, path, hash). The parser must populate the
    normalization fields it can determine (page_count, sheet_names,
    detected_schema) and return the updated document inside ParseResult.
    """

    @abstractmethod
    def parse(self, file_path: Path, file_doc: FileDocument) -> ParseResult:
        """Parse a file and return a normalized document object plus evidence chunks.

        Args:
            file_path: Absolute path to the uploaded file on disk.
            file_doc: The FileDocument metadata object for this file.
                The parser must populate normalization fields on this object.

        Returns:
            ParseResult containing the normalized document, evidence chunks,
            and any warnings.

        Raises:
            ParseError: If the file cannot be parsed at all.
        """
