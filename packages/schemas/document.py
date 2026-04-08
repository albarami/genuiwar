"""File document schema."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.schemas.enums import FileType


class FileDocument(BaseModel):
    """Metadata for an uploaded file."""

    file_id: UUID = Field(default_factory=uuid4)
    original_filename: str
    file_type: FileType
    file_size_bytes: int
    storage_path: str
    content_hash: str | None = None
    page_count: int | None = None
    sheet_names: list[str] | None = None
    detected_schema: dict[str, object] | None = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
