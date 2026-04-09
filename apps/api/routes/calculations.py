"""Calculation execution and result retrieval routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from packages.calculators import CalcRequest, CalculationEngine, CalculationError
from packages.schemas.calculation import CalculationResult

router = APIRouter(prefix="/calculations", tags=["calculations"])

_result_store: dict[UUID, CalculationResult] = {}
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

    _result_store[result.calculation_id] = result
    return result


@router.get("/{calculation_id}", response_model=CalculationResult)
async def get_calculation(calculation_id: UUID) -> CalculationResult:
    """Retrieve a stored calculation result by ID."""
    result = _result_store.get(calculation_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return result
