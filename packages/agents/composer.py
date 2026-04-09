"""Composer agent — builds the final structured answer from approved claims only."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.answer import AnswerBlock, AnswerBlockType, FinalAnswerPayload
from packages.schemas.claim import ClaimLedgerEntry


class ComposerInput(BaseModel):
    """Typed input for the Composer. Only approved + downgraded claims."""

    claims: list[ClaimLedgerEntry]
    run_id: UUID
    question: str


class DeterministicComposer(BaseAgent):
    """Rule-based Composer for tests."""

    @property
    def agent_name(self) -> str:
        return "composer"

    def execute(self, *, input: ComposerInput) -> FinalAnswerPayload:
        blocks: list[AnswerBlock] = []

        answer_text = "; ".join(c.claim_text for c in input.claims)
        claim_ids = [c.claim_id for c in input.claims]

        if answer_text:
            blocks.append(
                AnswerBlock(
                    block_type=AnswerBlockType.DIRECT_ANSWER,
                    content=answer_text,
                    claim_ids=claim_ids,
                )
            )

        blocks.append(
            AnswerBlock(
                block_type=AnswerBlockType.CONFIDENCE,
                content=f"{len(input.claims)} claims used in answer",
                claim_ids=claim_ids,
            )
        )

        return FinalAnswerPayload(
            run_id=input.run_id,
            blocks=blocks,
            approved_claim_ids=claim_ids,
            rejected_claim_ids=[],
            confidence_summary=f"Based on {len(input.claims)} approved/downgraded claims",
        )


class AzureComposer(BaseAgent):
    """Azure OpenAI-backed Composer."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "composer"

    def execute(self, *, input: ComposerInput) -> FinalAnswerPayload:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Composer. Build a structured final answer "
                "using ONLY the provided approved/downgraded claims. "
                "Every answer block must reference claim IDs. "
                "Never include information not backed by a claim."
            ),
            user_content=input.model_dump_json(),
            response_model=FinalAnswerPayload,
        )
