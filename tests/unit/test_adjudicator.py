"""Tests for Adjudicator — approve, downgrade, reject outcomes."""

from uuid import uuid4

from packages.agents.adjudicator import AdjudicatorInput, DeterministicAdjudicator
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.enums import (
    AdjudicationStatus,
    ChallengeFlag,
    ClaimType,
    SupportStatus,
)


def _claim(**kw) -> ClaimLedgerEntry:  # type: ignore[no-untyped-def]
    defaults = {
        "run_id": uuid4(),
        "claim_text": "Test",
        "claim_type": ClaimType.DIRECT,
        "support_status": SupportStatus.SUPPORTED,
        "evidence_refs": [uuid4()],
        "created_by_agent": "primary_analyst",
    }
    defaults.update(kw)
    return ClaimLedgerEntry(**defaults)


class TestDeterministicAdjudicator:
    def test_approved_when_no_flags(self) -> None:
        adj = DeterministicAdjudicator()
        result = adj.execute(input=AdjudicatorInput(claims=[_claim()]))
        assert result.adjudicated_claims[0].adjudication_status == AdjudicationStatus.APPROVED

    def test_rejected_when_unsupported(self) -> None:
        adj = DeterministicAdjudicator()
        result = adj.execute(
            input=AdjudicatorInput(
                claims=[_claim(support_status=SupportStatus.UNSUPPORTED)]
            )
        )
        assert result.adjudicated_claims[0].adjudication_status == AdjudicationStatus.REJECTED

    def test_rejected_when_missing_evidence_flag(self) -> None:
        adj = DeterministicAdjudicator()
        result = adj.execute(
            input=AdjudicatorInput(
                claims=[_claim(challenge_flags=[ChallengeFlag.MISSING_EVIDENCE])]
            )
        )
        assert result.adjudicated_claims[0].adjudication_status == AdjudicationStatus.REJECTED

    def test_downgraded_when_other_flags(self) -> None:
        adj = DeterministicAdjudicator()
        result = adj.execute(
            input=AdjudicatorInput(
                claims=[_claim(challenge_flags=[ChallengeFlag.WEAK_INTERPRETATION])]
            )
        )
        assert result.adjudicated_claims[0].adjudication_status == AdjudicationStatus.DOWNGRADED

    def test_adjudication_reason_always_set(self) -> None:
        adj = DeterministicAdjudicator()
        result = adj.execute(input=AdjudicatorInput(claims=[_claim()]))
        assert result.adjudicated_claims[0].adjudication_reason is not None
