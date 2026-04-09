"""Tests for DatasetContext builder/loader."""

from uuid import uuid4

from packages.agents.context_loader import build_dataset_context
from packages.schemas.dataset_context import (
    DatasetContext,
    EvidenceSourceType,
    FieldDefinition,
    FieldType,
    SourceLocator,
    TableContext,
)
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType


class TestContextLoader:
    def test_builds_from_xlsx_metadata(self) -> None:
        doc = FileDocument(
            original_filename="budget.xlsx",
            file_type=FileType.XLSX,
            file_size_bytes=1000,
            storage_path="/tmp/budget.xlsx",
            sheet_names=["Q1", "Q2"],
            detected_schema={
                "headers_by_sheet": {
                    "Q1": ["EID", "amount", "date"],
                    "Q2": ["EID", "amount"],
                },
            },
        )
        ctx = build_dataset_context([doc])

        assert len(ctx.tables) == 2
        assert ctx.tables[0].evidence_type == EvidenceSourceType.QUANTITATIVE
        assert len(ctx.identifier_rules) >= 2

    def test_builds_from_csv_metadata(self) -> None:
        doc = FileDocument(
            original_filename="data.csv",
            file_type=FileType.CSV,
            file_size_bytes=500,
            storage_path="/tmp/data.csv",
            detected_schema={"headers": ["name", "EID", "salary"]},
        )
        ctx = build_dataset_context([doc])

        assert len(ctx.tables) == 1
        eid_fields = [
            f
            for f in ctx.tables[0].fields
            if f.field_type == FieldType.IDENTIFIER
        ]
        assert len(eid_fields) >= 1

    def test_user_dict_takes_precedence(self) -> None:
        fid = uuid4()
        user_dict = DatasetContext(
            tables=[
                TableContext(
                    table_name="establishments",
                    source=SourceLocator(file_id=fid),
                    fields=[
                        FieldDefinition(
                            source_field_name="EID",
                            semantic_name="establishment_eid",
                            field_type=FieldType.IDENTIFIER,
                            identifier_scope="establishment",
                        )
                    ],
                )
            ],
            quantitative_sources=[fid],
        )
        doc = FileDocument(
            original_filename="est.xlsx",
            file_type=FileType.XLSX,
            file_size_bytes=100,
            storage_path="/tmp/est.xlsx",
        )
        ctx = build_dataset_context([doc], user_data_dictionary=user_dict)

        assert ctx.tables[0].table_name == "establishments"
        assert (
            ctx.tables[0].fields[0].semantic_name == "establishment_eid"
        )

    def test_docx_classified_as_qualitative(self) -> None:
        doc = FileDocument(
            original_filename="interview.docx",
            file_type=FileType.DOCX,
            file_size_bytes=100,
            storage_path="/tmp/interview.docx",
        )
        ctx = build_dataset_context([doc])

        assert ctx.tables[0].evidence_type == EvidenceSourceType.QUALITATIVE
        assert doc.file_id in ctx.qualitative_sources

    def test_always_includes_default_identifier_rules(self) -> None:
        ctx = build_dataset_context([])
        assert len(ctx.identifier_rules) >= 2
        patterns = {r.pattern for r in ctx.identifier_rules}
        assert "eid" in patterns
        assert "qid" in patterns

    def test_user_dict_enriched_with_parsed_gaps(self) -> None:
        fid = uuid4()
        user_dict = DatasetContext(
            tables=[
                TableContext(
                    table_name="data.csv",
                    source=SourceLocator(file_id=fid),
                    fields=[
                        FieldDefinition(
                            source_field_name="EID",
                            semantic_name="establishment_eid",
                            field_type=FieldType.IDENTIFIER,
                            identifier_scope="establishment",
                        )
                    ],
                )
            ],
            quantitative_sources=[fid],
        )
        doc = FileDocument(
            original_filename="data.csv",
            file_type=FileType.CSV,
            file_size_bytes=100,
            storage_path="/tmp/data.csv",
            detected_schema={"headers": ["EID", "salary", "date"]},
        )
        ctx = build_dataset_context([doc], user_data_dictionary=user_dict)

        table = ctx.tables[0]
        assert table.table_name == "data.csv"
        assert table.fields[0].semantic_name == "establishment_eid"
        field_names = {f.source_field_name for f in table.fields}
        assert "salary" in field_names
        assert "date" in field_names

    def test_user_dict_fields_not_overridden(self) -> None:
        fid = uuid4()
        user_dict = DatasetContext(
            tables=[
                TableContext(
                    table_name="data.csv",
                    source=SourceLocator(file_id=fid),
                    fields=[
                        FieldDefinition(
                            source_field_name="EID",
                            semantic_name="my_custom_meaning",
                            field_type=FieldType.IDENTIFIER,
                        )
                    ],
                )
            ],
        )
        doc = FileDocument(
            original_filename="data.csv",
            file_type=FileType.CSV,
            file_size_bytes=100,
            storage_path="/tmp/data.csv",
            detected_schema={"headers": ["EID", "value"]},
        )
        ctx = build_dataset_context([doc], user_data_dictionary=user_dict)

        eid_field = next(
            f for f in ctx.tables[0].fields
            if f.source_field_name == "EID"
        )
        assert eid_field.semantic_name == "my_custom_meaning"
