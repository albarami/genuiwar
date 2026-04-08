"""Claim ledger entry schema."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.schemas.enums import (
    AdjudicationStatus,
    ChallengeFlag,
    ClaimType,
    ConfidenceGrade,
    Materiality,
    SupportStatus,
)


class ClaimLedgerEntry(BaseModel):
    """A single claim tracked through the evidence-challenge-adjudication lifecycle."""

    claim_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    parent_claim_id: UUID | None = None
    claim_text: str
    claim_type: ClaimType
    claim_scope: str | None = None
    support_status: SupportStatus = SupportStatus.UNSUPPORTED
    confidence_grade: ConfidenceGrade = ConfidenceGrade.UNRESOLVED
    materiality: Materiality = Materiality.MEDIUM
    evidence_refs: list[UUID] = Field(default_factory=list)
    calculation_result_ids: list[UUID] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    challenge_flags: list[ChallengeFlag] = Field(default_factory=list)
    adjudication_status: AdjudicationStatus = AdjudicationStatus.PENDING
    adjudication_reason: str | None = None
    created_by_agent: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
