"""No-free-facts governance validators."""

from packages.schemas.answer import FinalAnswerPayload
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.enums import AdjudicationStatus

_COMPOSABLE = {AdjudicationStatus.APPROVED, AdjudicationStatus.DOWNGRADED}


def validate_claims_safe_for_composition(
    claims: list[ClaimLedgerEntry],
) -> list[str]:
    """Pre-compose check: all claims must be approved or downgraded."""
    violations: list[str] = []
    for claim in claims:
        if claim.adjudication_status not in _COMPOSABLE:
            violations.append(
                f"Claim {claim.claim_id} has status "
                f"{claim.adjudication_status}; not safe for composition"
            )
    return violations


def validate_answer_no_free_facts(
    answer: FinalAnswerPayload,
    approved_claims: list[ClaimLedgerEntry],
) -> list[str]:
    """Post-compose check: every answer block must map to approved/downgraded claims."""
    valid_ids = {c.claim_id for c in approved_claims}
    violations: list[str] = []

    for block in answer.blocks:
        if not block.claim_ids:
            violations.append(
                f"Answer block '{block.block_type}' has no supporting claim IDs"
            )
            continue
        for cid in block.claim_ids:
            if cid not in valid_ids:
                violations.append(
                    f"Answer block '{block.block_type}' references "
                    f"claim {cid} which is not approved/downgraded"
                )

    return violations
