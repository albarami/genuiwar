"""Tests for DatasetContext construction and field lookup."""

from uuid import uuid4

from packages.schemas.dataset_context import (
    DatasetContext,
    EvidenceSourceType,
    FieldDefinition,
    FieldType,
    JoinRule,
    JoinType,
    SourceLocator,
    TableContext,
)


class TestDatasetContext:
    def test_create_empty_context(self) -> None:
        ctx = DatasetContext()
        assert ctx.tables == []
        assert ctx.join_rules == []

    def test_create_with_tables(self) -> None:
        fid = uuid4()
        ctx = DatasetContext(
            tables=[
                TableContext(
                    table_name="headcount",
                    source=SourceLocator(file_id=fid, sheet_name="Sheet1"),
                    fields=[
                        FieldDefinition(
                            source_field_name="eid",
                            field_type=FieldType.IDENTIFIER,
                            identifier_scope="establishment",
                        ),
                        FieldDefinition(
                            source_field_name="count",
                            field_type=FieldType.NUMERIC,
                        ),
                    ],
                    evidence_type=EvidenceSourceType.QUANTITATIVE,
                )
            ],
            quantitative_sources=[fid],
        )
        assert len(ctx.tables) == 1
        assert ctx.tables[0].fields[0].field_type == FieldType.IDENTIFIER

    def test_join_rule_typing(self) -> None:
        rule = JoinRule(
            source_table="establishments",
            source_field="eid",
            target_table="employees",
            target_field="eid",
            join_type=JoinType.LEFT,
            description="Link employees to establishments",
        )
        assert rule.join_type == JoinType.LEFT

    def test_source_locator_with_sheet(self) -> None:
        loc = SourceLocator(
            file_id=uuid4(), sheet_name="Budget", table_name="Q1_budget"
        )
        assert loc.sheet_name == "Budget"
        assert loc.table_name == "Q1_budget"

    def test_evidence_source_type_enum(self) -> None:
        ctx = DatasetContext(
            tables=[
                TableContext(
                    table_name="interviews",
                    source=SourceLocator(file_id=uuid4()),
                    evidence_type=EvidenceSourceType.QUALITATIVE,
                )
            ]
        )
        assert ctx.tables[0].evidence_type == EvidenceSourceType.QUALITATIVE

    def test_identifier_rules_typed(self) -> None:
        from packages.schemas.dataset_context import IdentifierRule

        ctx = DatasetContext(
            identifier_rules=[
                IdentifierRule(
                    pattern="eid",
                    scope="establishment",
                    description="Per-table; do not assume global scope",
                ),
                IdentifierRule(pattern="qid", scope="person"),
            ]
        )
        assert len(ctx.identifier_rules) == 2
        assert ctx.identifier_rules[0].scope == "establishment"

    def test_field_semantic_name(self) -> None:
        field = FieldDefinition(
            source_field_name="EID",
            semantic_name="establishment_eid",
            field_type=FieldType.IDENTIFIER,
            identifier_scope="establishment",
        )
        assert field.source_field_name == "EID"
        assert field.semantic_name == "establishment_eid"
