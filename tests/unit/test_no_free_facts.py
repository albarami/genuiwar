"""Tests for no-free-facts governance validators."""

from uuid import uuid4

from packages.governance.no_free_facts import (
    validate_answer_no_free_facts,
    validate_claims_safe_for_composition,
)
from packages.schemas.answer import AnswerBlock, AnswerBlockType, FinalAnswerPayload
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.enums import AdjudicationStatus, ClaimType, SupportStatus


def _claim(status: AdjudicationStatus) -> ClaimLedgerEntry:
    return ClaimLedgerEntry(
        run_id=uuid4(),
        claim_text="Test",
        claim_type=ClaimType.DIRECT,
        support_status=SupportStatus.SUPPORTED,
        adjudication_status=status,
        created_by_agent="test",
    )


class TestPreComposeValidation:
    def test_pass_when_all_approved(self) -> None:
        claims = [_claim(AdjudicationStatus.APPROVED)]
        assert validate_claims_safe_for_composition(claims) == []

    def test_pass_when_downgraded(self) -> None:
        claims = [_claim(AdjudicationStatus.DOWNGRADED)]
        assert validate_claims_safe_for_composition(claims) == []

    def test_fail_when_rejected(self) -> None:
        claims = [_claim(AdjudicationStatus.REJECTED)]
        violations = validate_claims_safe_for_composition(claims)
        assert len(violations) == 1

    def test_fail_when_pending(self) -> None:
        claims = [_claim(AdjudicationStatus.PENDING)]
        violations = validate_claims_safe_for_composition(claims)
        assert len(violations) == 1


class TestPostComposeValidation:
    def test_pass_when_blocks_map_to_claims(self) -> None:
        claim = _claim(AdjudicationStatus.APPROVED)
        answer = FinalAnswerPayload(
            run_id=uuid4(),
            blocks=[
                AnswerBlock(
                    block_type=AnswerBlockType.DIRECT_ANSWER,
                    content="Result",
                    claim_ids=[claim.claim_id],
                )
            ],
        )
        assert validate_answer_no_free_facts(answer, [claim]) == []

    def test_fail_when_block_has_no_claim_ids(self) -> None:
        answer = FinalAnswerPayload(
            run_id=uuid4(),
            blocks=[
                AnswerBlock(
                    block_type=AnswerBlockType.DIRECT_ANSWER,
                    content="Free fact!",
                    claim_ids=[],
                )
            ],
        )
        violations = validate_answer_no_free_facts(answer, [])
        assert len(violations) >= 1

    def test_fail_when_claim_id_not_in_approved(self) -> None:
        answer = FinalAnswerPayload(
            run_id=uuid4(),
            blocks=[
                AnswerBlock(
                    block_type=AnswerBlockType.DIRECT_ANSWER,
                    content="Result",
                    claim_ids=[uuid4()],
                )
            ],
        )
        violations = validate_answer_no_free_facts(answer, [])
        assert len(violations) >= 1
