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
        raw = file_path.read_bytes()
        text: str | None = None
        for enc in ("utf-8", "latin-1"):
            try:
                text = raw.decode(enc)
                break
            except (UnicodeDecodeError, ValueError):
                continue
        if text is None:
            raise ParseError(str(file_path), "Cannot decode CSV as text")

        sample = raw[:1024]
        nul_count = sample.count(b"\x00")
        printable = sum(
            1 for b in sample if 0x20 <= b <= 0x7E or b in (0x09, 0x0A, 0x0D)
        )
        if nul_count > 0 or (len(sample) > 0 and printable / len(sample) < 0.5):
            raise ParseError(str(file_path), "File appears to be binary, not CSV")

        if not text.strip():
            return ParseResult(document=file_doc, warnings=["CSV file is empty"])

        try:
            dialect = csv.Sniffer().sniff(text[:4096])
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(StringIO(text), dialect)
        rows = list(reader)

        if not rows:
            return ParseResult(document=file_doc, warnings=["CSV file has no rows"])

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

        file_doc.detected_schema = {"headers": headers}

        return ParseResult(document=file_doc, chunks=chunks)
