"""DatasetContext builder — constructs schema context from available sources.

Priority:
1. Hard-coded governance identifier rules (always included)
2. User-supplied data dictionary (authoritative for tables it covers)
3. Parsed file metadata (fills gaps for files not covered by user dict)
"""

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
    """Build DatasetContext by merging user dictionary + parsed metadata.

    User-supplied per-table semantics are authoritative where they exist.
    Parsed metadata fills gaps for files/tables not covered by the user dict.
    Default identifier rules are always included.
    """
    user_tables = {}
    user_join_rules = []
    user_id_rules: list[IdentifierRule] = []
    user_quant: list[UUID] = []
    user_qual: list[UUID] = []

    if user_data_dictionary:
        for t in user_data_dictionary.tables:
            user_tables[t.table_name] = t
        user_join_rules = list(user_data_dictionary.join_rules)
        user_id_rules = list(user_data_dictionary.identifier_rules)
        user_quant = list(user_data_dictionary.quantitative_sources)
        user_qual = list(user_data_dictionary.qualitative_sources)

    parsed_tables: list[TableContext] = []
    parsed_quant: list[UUID] = []
    parsed_qual: list[UUID] = []

    for doc in file_documents:
        evidence_type = _infer_evidence_type(doc)

        if evidence_type == EvidenceSourceType.QUANTITATIVE:
            parsed_quant.append(doc.file_id)
        else:
            parsed_qual.append(doc.file_id)

        if doc.sheet_names:
            for sheet in doc.sheet_names:
                name = f"{doc.original_filename}:{sheet}"
                if name in user_tables:
                    _enrich_table_fields(
                        user_tables[name], doc.detected_schema, sheet
                    )
                    continue
                fields = _fields_from_schema(doc.detected_schema, sheet)
                parsed_tables.append(
                    TableContext(
                        table_name=name,
                        source=SourceLocator(
                            file_id=doc.file_id, sheet_name=sheet
                        ),
                        description=f"Sheet '{sheet}' from {doc.original_filename}",
                        fields=fields,
                        evidence_type=evidence_type,
                    )
                )
        else:
            name = doc.original_filename
            if name in user_tables:
                _enrich_table_fields(
                    user_tables[name], doc.detected_schema, None
                )
                continue
            fields = _fields_from_schema(doc.detected_schema, None)
            parsed_tables.append(
                TableContext(
                    table_name=name,
                    source=SourceLocator(file_id=doc.file_id),
                    description=f"Parsed from {doc.original_filename}",
                    fields=fields,
                    evidence_type=evidence_type,
                )
            )

    all_tables = list(user_tables.values()) + parsed_tables

    all_quant = list(set(user_quant + parsed_quant))
    all_qual = list(set(user_qual + parsed_qual))

    return DatasetContext(
        tables=all_tables,
        join_rules=user_join_rules,
        identifier_rules=list(_DEFAULT_IDENTIFIER_RULES) + user_id_rules,
        quantitative_sources=all_quant,
        qualitative_sources=all_qual,
    )


def _enrich_table_fields(
    table: TableContext,
    detected_schema: dict[str, object] | None,
    sheet_name: str | None,
) -> None:
    """Fill missing fields on a user-supplied table from parsed metadata.

    Never overrides existing user-defined fields.
    """
    if not detected_schema:
        return

    existing_names = {f.source_field_name.lower() for f in table.fields}
    parsed = _fields_from_schema(detected_schema, sheet_name)

    for field in parsed:
        if field.source_field_name.lower() not in existing_names:
            table.fields.append(field)


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
    """Conservative field-type guess from column name."""
    lower = name.lower()
    if lower in ("eid", "qid", "id", "person_id", "est_id"):
        return FieldType.IDENTIFIER
    if "date" in lower or "time" in lower:
        return FieldType.DATE
    return FieldType.TEXT
