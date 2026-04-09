"""Evidence chunk and bundle schemas."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CitationAnchor(BaseModel):
    """Locator for a specific position within a source file."""

    file_id: UUID
    page: int | None = None
    section: str | None = None
    row_range: tuple[int, int] | None = None
    sheet_name: str | None = None


class EvidenceChunk(BaseModel):
    """A discrete piece of evidence extracted from a source file."""

    chunk_id: UUID = Field(default_factory=uuid4)
    file_id: UUID
    content: str
    content_type: str = "text"
    citation_anchor: CitationAnchor
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class EvidenceBundle(BaseModel):
    """A set of evidence chunks selected for a specific query."""

    bundle_id: UUID = Field(default_factory=uuid4)
    query: str
    chunks: list[EvidenceChunk] = Field(default_factory=list)
    file_ids: list[UUID] = Field(default_factory=list)
    total_candidates: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
