"""Calculation execution and result retrieval routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.api.dependencies import calc_repo
from packages.calculators import CalcRequest, CalculationEngine, CalculationError
from packages.schemas.calculation import CalculationResult

router = APIRouter(prefix="/calculations", tags=["calculations"])

_engine = CalculationEngine()


@router.post("/execute", response_model=CalculationResult)
async def execute_calculation(req: CalcRequest) -> CalculationResult:
    """Execute a trusted calculation and return the typed result with trace."""
    try:
        result = _engine.execute(req)
    except CalculationError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Calculation error ({exc.operation}): {exc.reason}",
        ) from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid calculation inputs: {exc}",
        ) from exc

    calc_repo.save(result)
    return result


@router.get("/{calculation_id}", response_model=CalculationResult)
async def get_calculation(calculation_id: UUID) -> CalculationResult:
    """Retrieve a stored calculation result by ID."""
    result = calc_repo.get(calculation_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return result


class TraceResponse(BaseModel):
    """Typed response for the trace-only endpoint."""

    calculation_id: UUID
    operation: str
    trace: list[str]
    output_unit: str | None = None


@router.get("/{calculation_id}/trace", response_model=TraceResponse)
async def get_calculation_trace(
    calculation_id: UUID,
) -> TraceResponse:
    """Return only the trace payload for a calculation."""
    result = calc_repo.get(calculation_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return TraceResponse(
        calculation_id=result.calculation_id,
        operation=result.operation,
        trace=result.trace,
        output_unit=result.output_unit,
    )
