"""Run and RunEvent schemas."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.schemas.enums import EventGroup, RunCategory, RunMode, RunStatus


class Run(BaseModel):
    """A discrete analytical execution."""

    run_id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID
    trigger_message_id: UUID | None = None
    parent_run_id: UUID | None = None
    run_category: RunCategory
    run_mode: RunMode
    status: RunStatus = RunStatus.QUEUED
    scope: str | None = None
    question: str | None = None
    decision_reason: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None


class RunEvent(BaseModel):
    """A structured, streamable record of something meaningful during a run."""

    event_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    event_index: int
    event_type: str
    event_group: EventGroup
    agent_name: str | None = None
    status: str = "emitted"
    title: str
    summary: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    is_user_visible: bool = True
