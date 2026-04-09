"""Schema interpretation and data dictionary models."""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class FieldType(StrEnum):
    """Type classification for a table field."""

    IDENTIFIER = "identifier"
    DATE = "date"
    NUMERIC = "numeric"
    TEXT = "text"
    CATEGORICAL = "categorical"


class EvidenceSourceType(StrEnum):
    """Whether a data source is quantitative or qualitative."""

    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"


class JoinType(StrEnum):
    """Type of cross-table join."""

    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL = "full"


class SourceLocator(BaseModel):
    """Precise location of a table within a file."""

    file_id: UUID
    sheet_name: str | None = None
    table_name: str | None = None
    row_range: tuple[int, int] | None = None


class JoinRule(BaseModel):
    """Typed declaration of a valid cross-table join."""

    source_table: str
    source_field: str
    target_table: str
    target_field: str
    join_type: JoinType = JoinType.INNER
    description: str = ""


class FieldDefinition(BaseModel):
    """Definition of a single field within a table."""

    field_name: str
    description: str = ""
    field_type: FieldType
    identifier_scope: str | None = None
    is_joinable: bool = False


class TableContext(BaseModel):
    """Metadata for a single table/sheet in the dataset."""

    table_name: str
    source: SourceLocator
    description: str = ""
    fields: list[FieldDefinition] = Field(default_factory=list)
    evidence_type: EvidenceSourceType = EvidenceSourceType.QUANTITATIVE


class DatasetContext(BaseModel):
    """Full schema context for a set of uploaded files."""

    tables: list[TableContext] = Field(default_factory=list)
    join_rules: list[JoinRule] = Field(default_factory=list)
    identifier_rules: list[str] = Field(default_factory=list)
    qualitative_sources: list[UUID] = Field(default_factory=list)
    quantitative_sources: list[UUID] = Field(default_factory=list)
