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

_INFERRED_UNITS: dict[str, str] = {
    "percentage_change": "percent",
}


class CalcRequest(BaseModel):
    """Request to execute a trusted calculation."""

    operation: str
    inputs: dict[str, Any]
    input_units: dict[str, str] = Field(default_factory=dict)
    output_unit: str | None = None
    evidence_refs: list[UUID] = Field(default_factory=list)
    run_id: UUID | None = None


def _infer_output_unit(operation: str) -> str | None:
    """Return a default output unit for operations where it is unambiguous."""
    return _INFERRED_UNITS.get(operation)


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

        output_unit = request.output_unit or _infer_output_unit(op)

        if output_unit:
            trace.append(f"output unit: {output_unit}")

        return CalculationResult(
            run_id=run_id,
            operation=op,
            inputs=inputs,
            result=result_val,
            trace=trace,
            input_units=request.input_units,
            output_unit=output_unit,
            evidence_refs=request.evidence_refs,
        )
