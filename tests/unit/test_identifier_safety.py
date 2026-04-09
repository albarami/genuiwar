"""Tests for identifier safety governance."""

from uuid import uuid4

from packages.governance.identifier_safety import validate_identifier_usage
from packages.schemas.claim import ClaimLedgerEntry
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
from packages.schemas.enums import ClaimType, SupportStatus


def _claim(text: str) -> ClaimLedgerEntry:
    return ClaimLedgerEntry(
        run_id=uuid4(),
        claim_text=text,
        claim_type=ClaimType.DIRECT,
        support_status=SupportStatus.SUPPORTED,
        created_by_agent="test",
    )


def _ctx_with_shared_eid() -> DatasetContext:
    fid = uuid4()
    return DatasetContext(
        tables=[
            TableContext(
                table_name="establishments",
                source=SourceLocator(file_id=fid),
                fields=[
                    FieldDefinition(
                        field_name="eid",
                        field_type=FieldType.IDENTIFIER,
                        identifier_scope="establishment",
                    )
                ],
            ),
            TableContext(
                table_name="employees",
                source=SourceLocator(file_id=fid),
                fields=[
                    FieldDefinition(
                        field_name="eid",
                        field_type=FieldType.IDENTIFIER,
                        identifier_scope="establishment",
                    )
                ],
            ),
        ],
    )


class TestIdentifierSafety:
    def test_no_violations_when_join_declared(self) -> None:
        ctx = _ctx_with_shared_eid()
        ctx.join_rules = [
            JoinRule(
                source_table="establishments",
                source_field="eid",
                target_table="employees",
                target_field="eid",
                join_type=JoinType.INNER,
            )
        ]
        violations = validate_identifier_usage([_claim("test")], ctx)
        assert violations == []

    def test_violation_when_no_join_declared(self) -> None:
        ctx = _ctx_with_shared_eid()
        violations = validate_identifier_usage([_claim("test")], ctx)
        assert len(violations) >= 1
        assert "eid" in violations[0].lower()

    def test_no_violation_when_single_table(self) -> None:
        fid = uuid4()
        ctx = DatasetContext(
            tables=[
                TableContext(
                    table_name="data",
                    source=SourceLocator(file_id=fid),
                    fields=[
                        FieldDefinition(
                            field_name="eid",
                            field_type=FieldType.IDENTIFIER,
                        )
                    ],
                )
            ]
        )
        violations = validate_identifier_usage([_claim("test")], ctx)
        assert violations == []

    def test_qualitative_quantitative_mixing_flagged(self) -> None:
        fid = uuid4()
        ctx = DatasetContext(
            tables=[
                TableContext(
                    table_name="interviews",
                    source=SourceLocator(file_id=fid),
                    evidence_type=EvidenceSourceType.QUALITATIVE,
                ),
                TableContext(
                    table_name="budget",
                    source=SourceLocator(file_id=fid),
                    evidence_type=EvidenceSourceType.QUANTITATIVE,
                ),
            ]
        )
        claim = _claim("Based on interviews and budget data")
        violations = validate_identifier_usage([claim], ctx)
        assert len(violations) >= 1
        assert "qualitative" in violations[0].lower()
