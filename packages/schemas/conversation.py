"""Conversation and Message schemas."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.schemas.enums import MessageRole


class Message(BaseModel):
    """A single message within a conversation."""

    message_id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID
    role: MessageRole
    content: str
    run_id: UUID | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class Conversation(BaseModel):
    """A conversation session containing messages and file attachments."""

    conversation_id: UUID = Field(default_factory=uuid4)
    title: str | None = None
    file_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
