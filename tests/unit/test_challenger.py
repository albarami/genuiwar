"""Tests for Challenger — flagging high-materiality claims."""

from uuid import uuid4

from packages.agents.challenger import ChallengerInput, DeterministicChallenger
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import ClaimType, Materiality, SupportStatus
from packages.schemas.evidence import EvidenceBundle


def _claim(materiality: Materiality = Materiality.MEDIUM, **kw) -> ClaimLedgerEntry:  # type: ignore[no-untyped-def]
    return ClaimLedgerEntry(
        run_id=uuid4(),
        claim_text="Test claim",
        claim_type=ClaimType.DIRECT,
        support_status=SupportStatus.SUPPORTED,
        materiality=materiality,
        evidence_refs=[uuid4()],
        created_by_agent="primary_analyst",
        **kw,
    )


class TestDeterministicChallenger:
    def test_high_materiality_gets_flagged(self) -> None:
        challenger = DeterministicChallenger()
        result = challenger.execute(
            input=ChallengerInput(
                claims=[_claim(Materiality.HIGH)],
                evidence_bundle=EvidenceBundle(query="Q?", total_candidates=0),
                dataset_context=DatasetContext(),
            )
        )
        assert len(result.reviewed_claims[0].challenge_flags) >= 1

    def test_medium_materiality_no_flag_added(self) -> None:
        challenger = DeterministicChallenger()
        result = challenger.execute(
            input=ChallengerInput(
                claims=[_claim(Materiality.MEDIUM)],
                evidence_bundle=EvidenceBundle(query="Q?", total_candidates=0),
                dataset_context=DatasetContext(),
            )
        )
        assert result.reviewed_claims[0].challenge_flags == []

    def test_high_materiality_missing_evidence_flagged(self) -> None:
        claim = _claim(Materiality.HIGH)
        claim.evidence_refs = []
        challenger = DeterministicChallenger()
        result = challenger.execute(
            input=ChallengerInput(
                claims=[claim],
                evidence_bundle=EvidenceBundle(query="Q?", total_candidates=0),
                dataset_context=DatasetContext(),
            )
        )
        flags = result.reviewed_claims[0].challenge_flags
        assert "missing_evidence" in [str(f) for f in flags]
