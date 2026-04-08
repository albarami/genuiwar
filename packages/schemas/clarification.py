"""Clarification request schema."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ClarificationRequest(BaseModel):
    """A structured question the system asks the user when it cannot proceed safely."""

    clarification_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    question: str
    reason: str
    options: list[str] = Field(default_factory=list)
    response: str | None = None
    responded_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
