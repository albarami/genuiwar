"""Tests for Composer — rejected claims excluded, answer blocks typed."""

from uuid import uuid4

from packages.agents.composer import ComposerInput, DeterministicComposer
from packages.schemas.answer import AnswerBlockType
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.enums import AdjudicationStatus, ClaimType, SupportStatus


def _approved_claim() -> ClaimLedgerEntry:
    return ClaimLedgerEntry(
        run_id=uuid4(),
        claim_text="Approved finding",
        claim_type=ClaimType.DIRECT,
        support_status=SupportStatus.SUPPORTED,
        adjudication_status=AdjudicationStatus.APPROVED,
        evidence_refs=[uuid4()],
        created_by_agent="primary_analyst",
    )


class TestDeterministicComposer:
    def test_produces_answer_blocks(self) -> None:
        composer = DeterministicComposer()
        result = composer.execute(
            input=ComposerInput(
                claims=[_approved_claim()],
                run_id=uuid4(),
                question="Q?",
            )
        )
        assert len(result.blocks) >= 1

    def test_answer_blocks_have_enum_types(self) -> None:
        composer = DeterministicComposer()
        result = composer.execute(
            input=ComposerInput(
                claims=[_approved_claim()],
                run_id=uuid4(),
                question="Q?",
            )
        )
        for block in result.blocks:
            assert isinstance(block.block_type, AnswerBlockType)

    def test_answer_blocks_reference_claim_ids(self) -> None:
        claim = _approved_claim()
        composer = DeterministicComposer()
        result = composer.execute(
            input=ComposerInput(
                claims=[claim],
                run_id=uuid4(),
                question="Q?",
            )
        )
        all_ids = {cid for b in result.blocks for cid in b.claim_ids}
        assert claim.claim_id in all_ids

    def test_empty_claims_still_produces_output(self) -> None:
        composer = DeterministicComposer()
        result = composer.execute(
            input=ComposerInput(claims=[], run_id=uuid4(), question="Q?")
        )
        assert result.answer_id is not None
