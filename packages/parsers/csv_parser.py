"""CSV parser — header detection and row-based chunking."""

import csv
from io import StringIO
from pathlib import Path

from packages.parsers.base import BaseParser, ParseError, ParseResult
from packages.parsers.registry import register_parser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType
from packages.schemas.evidence import CitationAnchor, EvidenceChunk

_CHUNK_ROW_SIZE = 50


@register_parser(FileType.CSV)
class CsvParser(BaseParser):
    """Parse .csv files into evidence chunks with row-range citation anchors."""

    def parse(self, file_path: Path, file_doc: FileDocument) -> ParseResult:
        """Parse a CSV file into evidence chunks."""
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                text = file_path.read_text(encoding="latin-1")
            except Exception as exc:
                raise ParseError(str(file_path), f"Cannot decode CSV: {exc}") from exc
        except Exception as exc:
            raise ParseError(str(file_path), f"Cannot read CSV: {exc}") from exc

        if not text.strip():
            return ParseResult(warnings=["CSV file is empty"])

        try:
            dialect = csv.Sniffer().sniff(text[:4096])
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(StringIO(text), dialect)
        rows = list(reader)

        if not rows:
            return ParseResult(warnings=["CSV file has no rows"])

        headers = rows[0]
        chunks: list[EvidenceChunk] = []

        for start in range(0, len(rows), _CHUNK_ROW_SIZE):
            batch = rows[start : start + _CHUNK_ROW_SIZE]
            lines = [" | ".join(r) for r in batch]
            end = min(start + _CHUNK_ROW_SIZE, len(rows))

            chunks.append(
                EvidenceChunk(
                    file_id=file_doc.file_id,
                    content="\n".join(lines),
                    content_type="table",
                    citation_anchor=CitationAnchor(
                        file_id=file_doc.file_id,
                        row_range=(start + 1, end),
                    ),
                    metadata={
                        "headers": " | ".join(headers),
                    },
                )
            )

        return ParseResult(
            chunks=chunks,
            metadata={"row_count": len(rows), "headers": headers},
        )
