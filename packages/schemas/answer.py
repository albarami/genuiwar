"""Final answer payload schema."""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AnswerBlockType(StrEnum):
    """Type of block in a structured final answer."""

    DIRECT_ANSWER = "direct_answer"
    EVIDENCE = "evidence"
    CONFIDENCE = "confidence"
    DEBATE_SUMMARY = "debate_summary"
    CALCULATION = "calculation"
    CITATIONS = "citations"


class AnswerBlock(BaseModel):
    """A single block in the structured final answer."""

    block_type: AnswerBlockType
    content: str
    claim_ids: list[UUID] = Field(default_factory=list)


class FinalAnswerPayload(BaseModel):
    """The complete structured answer produced by the Composer agent."""

    answer_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    blocks: list[AnswerBlock] = Field(default_factory=list)
    approved_claim_ids: list[UUID] = Field(default_factory=list)
    rejected_claim_ids: list[UUID] = Field(default_factory=list)
    confidence_summary: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
