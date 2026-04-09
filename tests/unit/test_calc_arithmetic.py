"""Tests for arithmetic operations — add, subtract, multiply, divide, errors."""

import pytest

from packages.calculators.operations import CalculationError, arithmetic


class TestArithmetic:
    def test_add(self) -> None:
        result, trace = arithmetic(10, 3, "add")
        assert result == 13
        assert "10" in trace[0] and "13" in trace[0]

    def test_subtract(self) -> None:
        result, trace = arithmetic(10, 3, "subtract")
        assert result == 7
        assert len(trace) == 1

    def test_multiply(self) -> None:
        result, _ = arithmetic(4, 5, "multiply")
        assert result == 20

    def test_divide(self) -> None:
        result, _ = arithmetic(10, 4, "divide")
        assert result == 2.5

    def test_divide_by_zero(self) -> None:
        with pytest.raises(CalculationError, match="Division by zero"):
            arithmetic(10, 0, "divide")

    def test_unknown_operator(self) -> None:
        with pytest.raises(CalculationError, match="Unknown operator"):
            arithmetic(1, 2, "modulo")

    def test_negative_numbers(self) -> None:
        result, _ = arithmetic(-5, 3, "add")
        assert result == -2

    def test_trace_present(self) -> None:
        _, trace = arithmetic(7, 2, "multiply")
        assert len(trace) >= 1
        assert "14" in trace[0]
