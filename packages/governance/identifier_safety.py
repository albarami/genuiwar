"""Identifier and schema safety governance validators."""

from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.dataset_context import DatasetContext, EvidenceSourceType


def validate_identifier_usage(
    claims: list[ClaimLedgerEntry],
    context: DatasetContext,
) -> list[str]:
    """Check claims for identifier ambiguity, unsafe joins, and evidence mixing."""
    violations: list[str] = []

    declared_join_keys: set[tuple[str, str]] = set()
    for rule in context.join_rules:
        declared_join_keys.add((rule.source_table, rule.source_field))
        declared_join_keys.add((rule.target_table, rule.target_field))

    identifier_fields: dict[str, list[str]] = {}
    for table in context.tables:
        for field in table.fields:
            if field.field_type == "identifier":
                identifier_fields.setdefault(field.field_name.lower(), []).append(
                    table.table_name
                )

    for field_name, tables in identifier_fields.items():
        if len(tables) > 1:
            pair = (tables[0], field_name)
            if pair not in declared_join_keys:
                violations.append(
                    f"Identifier '{field_name}' appears in {tables} "
                    f"but no JoinRule declares how they relate"
                )

    qual_tables = {
        t.table_name
        for t in context.tables
        if t.evidence_type == EvidenceSourceType.QUALITATIVE
    }
    quant_tables = {
        t.table_name
        for t in context.tables
        if t.evidence_type == EvidenceSourceType.QUANTITATIVE
    }

    for claim in claims:
        text_lower = claim.claim_text.lower()
        for qt in qual_tables:
            if qt.lower() in text_lower and any(
                qnt.lower() in text_lower for qnt in quant_tables
            ):
                violations.append(
                    f"Claim {claim.claim_id} may mix qualitative "
                    f"({qt}) and quantitative evidence without distinction"
                )

    return violations
