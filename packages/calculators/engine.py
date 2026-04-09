"""Calculation engine — dispatches requests to operations and builds results."""

from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.calculators.operations import (
    CalculationError,
    arithmetic,
    compare,
    group_total,
    percentage_change,
    ratio,
    sum_values,
)
from packages.schemas.calculation import CalculationResult


class CalcRequest(BaseModel):
    """Request to execute a trusted calculation."""

    operation: str
    inputs: dict[str, Any]
    evidence_refs: list[UUID] = Field(default_factory=list)
    run_id: UUID | None = None


class CalculationEngine:
    """Dispatches calculation requests to pure-function operations."""

    def execute(self, request: CalcRequest) -> CalculationResult:
        """Execute a calculation and return a typed result with trace.

        Uses a request-scoped UUID as run_id if none is provided,
        keeping CalculationResult.run_id schema unchanged.
        """
        run_id = request.run_id or uuid4()
        op = request.operation
        inputs = request.inputs

        result_val: Any
        trace: list[str]

        if op in ("add", "subtract", "multiply", "divide"):
            result_val, trace = arithmetic(
                float(inputs["a"]),
                float(inputs["b"]),
                op,
            )
        elif op == "percentage_change":
            result_val, trace = percentage_change(
                float(inputs["old"]),
                float(inputs["new"]),
            )
        elif op == "ratio":
            result_val, trace = ratio(
                float(inputs["numerator"]),
                float(inputs["denominator"]),
            )
        elif op == "sum":
            result_val, trace = sum_values(
                [float(v) for v in inputs["values"]],
            )
        elif op == "group_total":
            result_val, trace = group_total(
                inputs["rows"],
                str(inputs["group_key"]),
                str(inputs["value_key"]),
            )
        elif op == "compare":
            result_val, trace = compare(
                float(inputs["a"]),
                float(inputs["b"]),
            )
        else:
            raise CalculationError(op, f"Unknown operation: {op}")

        return CalculationResult(
            run_id=run_id,
            operation=op,
            inputs=inputs,
            result=result_val,
            trace=trace,
            evidence_refs=request.evidence_refs,
        )
