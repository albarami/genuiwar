"""DatasetContext builder — constructs schema context from available sources."""

from __future__ import annotations

from uuid import UUID

from packages.schemas.dataset_context import (
    DatasetContext,
    EvidenceSourceType,
    FieldDefinition,
    FieldType,
    IdentifierRule,
    SourceLocator,
    TableContext,
)
from packages.schemas.document import FileDocument

_DEFAULT_IDENTIFIER_RULES = [
    IdentifierRule(
        pattern="eid",
        scope="establishment",
        description="Per-table; do not assume global scope",
    ),
    IdentifierRule(
        pattern="qid",
        scope="person",
        description="Per-table; do not assume global scope",
    ),
]


def build_dataset_context(
    file_documents: list[FileDocument],
    user_data_dictionary: DatasetContext | None = None,
) -> DatasetContext:
    """Build DatasetContext from available sources.

    Priority:
    1. Hard-coded governance identifier rules (always included)
    2. User-supplied data dictionary (if provided, its tables/join_rules take precedence)
    3. Parsed file metadata (fallback to fill gaps)
    """
    if user_data_dictionary and user_data_dictionary.tables:
        ctx = user_data_dictionary.model_copy(deep=True)
        ctx.identifier_rules = list(_DEFAULT_IDENTIFIER_RULES) + list(
            ctx.identifier_rules
        )
        return ctx

    tables: list[TableContext] = []
    quant_sources: list[UUID] = []
    qual_sources: list[UUID] = []

    for doc in file_documents:
        evidence_type = _infer_evidence_type(doc)

        if evidence_type == EvidenceSourceType.QUANTITATIVE:
            quant_sources.append(doc.file_id)
        else:
            qual_sources.append(doc.file_id)

        if doc.sheet_names:
            for sheet in doc.sheet_names:
                fields = _fields_from_schema(doc.detected_schema, sheet)
                tables.append(
                    TableContext(
                        table_name=f"{doc.original_filename}:{sheet}",
                        source=SourceLocator(
                            file_id=doc.file_id, sheet_name=sheet
                        ),
                        description=f"Sheet '{sheet}' from {doc.original_filename}",
                        fields=fields,
                        evidence_type=evidence_type,
                    )
                )
        else:
            fields = _fields_from_schema(doc.detected_schema, None)
            tables.append(
                TableContext(
                    table_name=doc.original_filename,
                    source=SourceLocator(file_id=doc.file_id),
                    description=f"Parsed from {doc.original_filename}",
                    fields=fields,
                    evidence_type=evidence_type,
                )
            )

    return DatasetContext(
        tables=tables,
        identifier_rules=list(_DEFAULT_IDENTIFIER_RULES),
        quantitative_sources=quant_sources,
        qualitative_sources=qual_sources,
    )


def _infer_evidence_type(doc: FileDocument) -> EvidenceSourceType:
    """Infer whether a file is quantitative or qualitative from its type."""
    if doc.file_type in ("xlsx", "csv"):
        return EvidenceSourceType.QUANTITATIVE
    if doc.file_type in ("docx", "pptx", "pdf"):
        return EvidenceSourceType.QUALITATIVE
    return EvidenceSourceType.QUANTITATIVE


def _fields_from_schema(
    detected_schema: dict[str, object] | None,
    sheet_name: str | None,
) -> list[FieldDefinition]:
    """Extract field definitions from parsed detected_schema metadata."""
    if not detected_schema:
        return []

    headers = detected_schema.get("headers")
    if sheet_name:
        by_sheet = detected_schema.get("headers_by_sheet")
        if isinstance(by_sheet, dict):
            headers = by_sheet.get(sheet_name, headers)

    if not isinstance(headers, list):
        return []

    fields: list[FieldDefinition] = []
    for h in headers:
        name = str(h)
        ft = _guess_field_type(name)
        fields.append(
            FieldDefinition(
                source_field_name=name,
                field_type=ft,
                identifier_scope="unknown" if ft == FieldType.IDENTIFIER else None,
            )
        )
    return fields


def _guess_field_type(name: str) -> FieldType:
    """Conservative field-type guess from column name. Flags identifiers."""
    lower = name.lower()
    if lower in ("eid", "qid", "id", "person_id", "est_id"):
        return FieldType.IDENTIFIER
    if "date" in lower or "time" in lower:
        return FieldType.DATE
    return FieldType.TEXT
