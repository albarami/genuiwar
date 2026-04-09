"""PDF parser — extracts text and tables page-by-page."""

from pathlib import Path

import pdfplumber

from packages.parsers.base import BaseParser, ParseError, ParseResult
from packages.parsers.registry import register_parser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType
from packages.schemas.evidence import CitationAnchor, EvidenceChunk


@register_parser(FileType.PDF)
class PdfParser(BaseParser):
    """Parse .pdf files into evidence chunks with page-based citation anchors."""

    def parse(self, file_path: Path, file_doc: FileDocument) -> ParseResult:
        """Parse a PDF file into evidence chunks."""
        try:
            pdf = pdfplumber.open(str(file_path))
        except Exception as exc:
            raise ParseError(str(file_path), f"Cannot open PDF: {exc}") from exc

        chunks: list[EvidenceChunk] = []
        warnings: list[str] = []

        try:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    chunks.append(
                        EvidenceChunk(
                            file_id=file_doc.file_id,
                            content=text.strip(),
                            content_type="text",
                            citation_anchor=CitationAnchor(
                                file_id=file_doc.file_id,
                                page=page_num,
                            ),
                        )
                    )

                tables = page.extract_tables()
                for tbl_idx, table_data in enumerate(tables or []):
                    rows_text: list[str] = []
                    for row in table_data:
                        cells = [(c or "").strip() for c in row]
                        rows_text.append(" | ".join(cells))
                    if rows_text:
                        chunks.append(
                            EvidenceChunk(
                                file_id=file_doc.file_id,
                                content="\n".join(rows_text),
                                content_type="table",
                                citation_anchor=CitationAnchor(
                                    file_id=file_doc.file_id,
                                    page=page_num,
                                ),
                                metadata={
                                    "table_index": str(tbl_idx),
                                    "page": str(page_num),
                                },
                            )
                        )
        finally:
            pdf.close()

        if not chunks:
            warnings.append("PDF file produced no content chunks")

        return ParseResult(
            chunks=chunks,
            metadata={"page_count": len(pdf.pages)},
            warnings=warnings,
        )
