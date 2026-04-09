"""Calculation result schema."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CalculationResult(BaseModel):
    """Output of a trusted calculation with full trace."""

    calculation_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    operation: str
    inputs: dict[str, Any]
    result: Any
    trace: list[str] = Field(default_factory=list)
    input_units: dict[str, str] = Field(default_factory=dict)
    output_unit: str | None = None
    evidence_refs: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
