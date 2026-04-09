"""Tests for CalculationEngine — dispatch, trace, errors."""

from uuid import uuid4

import pytest

from packages.calculators import CalcRequest, CalculationEngine, CalculationError


class TestCalculationEngine:
    def test_dispatch_add(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="add", inputs={"a": 5, "b": 3})
        )
        assert result.result == 8
        assert result.operation == "add"

    def test_dispatch_percentage_change(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="percentage_change",
                inputs={"old": 100, "new": 120},
            )
        )
        assert result.result == 20.0

    def test_dispatch_sum(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="sum", inputs={"values": [10, 20, 30]})
        )
        assert result.result == 60

    def test_dispatch_compare(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="compare", inputs={"a": 100, "b": 80})
        )
        assert result.result["difference"] == 20

    def test_dispatch_group_total(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="group_total",
                inputs={
                    "rows": [
                        {"dept": "IT", "val": 10},
                        {"dept": "IT", "val": 20},
                    ],
                    "group_key": "dept",
                    "value_key": "val",
                },
            )
        )
        assert result.result["IT"] == 30

    def test_unknown_operation_raises(self) -> None:
        engine = CalculationEngine()
        with pytest.raises(CalculationError, match="Unknown operation"):
            engine.execute(
                CalcRequest(operation="magic", inputs={})
            )

    def test_divide_by_zero_raises(self) -> None:
        engine = CalculationEngine()
        with pytest.raises(CalculationError, match="Division by zero"):
            engine.execute(
                CalcRequest(operation="divide", inputs={"a": 10, "b": 0})
            )

    def test_trace_completeness(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="percentage_change",
                inputs={"old": 200, "new": 250},
            )
        )
        assert len(result.trace) >= 2
        assert any("old" in step for step in result.trace)
        assert any("new" in step for step in result.trace)

    def test_evidence_refs_preserved(self) -> None:
        ref = uuid4()
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="add",
                inputs={"a": 1, "b": 2},
                evidence_refs=[ref],
            )
        )
        assert ref in result.evidence_refs

    def test_run_id_generated_when_not_provided(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="add", inputs={"a": 1, "b": 1})
        )
        assert result.run_id is not None

    def test_run_id_used_when_provided(self) -> None:
        rid = uuid4()
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="add",
                inputs={"a": 1, "b": 1},
                run_id=rid,
            )
        )
        assert result.run_id == rid

    def test_missing_input_key_raises(self) -> None:
        engine = CalculationEngine()
        with pytest.raises(KeyError):
            engine.execute(
                CalcRequest(operation="add", inputs={"a": 1})
            )

    def test_percentage_change_has_percent_unit(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="percentage_change",
                inputs={"old": 100, "new": 120},
            )
        )
        assert result.output_unit == "percent"

    def test_explicit_output_unit_overrides_inferred(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="add",
                inputs={"a": 10, "b": 5},
                output_unit="SAR",
            )
        )
        assert result.output_unit == "SAR"
        assert any("SAR" in step for step in result.trace)

    def test_input_units_preserved(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="add",
                inputs={"a": 10, "b": 5},
                input_units={"a": "SAR", "b": "SAR"},
            )
        )
        assert result.input_units == {"a": "SAR", "b": "SAR"}

    def test_no_unit_when_not_applicable(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="compare", inputs={"a": 10, "b": 5})
        )
        assert result.output_unit is None

    def test_output_unit_appears_in_trace(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="percentage_change",
                inputs={"old": 50, "new": 75},
            )
        )
        assert any("output unit: percent" in step for step in result.trace)

    def test_input_units_appear_in_trace(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(
                operation="add",
                inputs={"a": 10, "b": 5},
                input_units={"a": "SAR", "b": "SAR"},
            )
        )
        assert any("input units:" in step for step in result.trace)
        assert any("SAR" in step for step in result.trace)

    def test_no_unit_lines_when_absent(self) -> None:
        engine = CalculationEngine()
        result = engine.execute(
            CalcRequest(operation="add", inputs={"a": 1, "b": 2})
        )
        for step in result.trace:
            assert "input units:" not in step
            assert "output unit:" not in step
