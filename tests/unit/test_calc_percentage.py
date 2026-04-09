"""Tests for percentage change and ratio operations."""

import pytest

from packages.calculators.operations import (
    CalculationError,
    percentage_change,
    ratio,
)


class TestPercentageChange:
    def test_positive_change(self) -> None:
        result, trace = percentage_change(100, 120)
        assert result == 20.0
        assert len(trace) >= 2

    def test_negative_change(self) -> None:
        result, _ = percentage_change(200, 150)
        assert result == -25.0

    def test_zero_base_raises(self) -> None:
        with pytest.raises(CalculationError, match="zero base"):
            percentage_change(0, 100)

    def test_no_change(self) -> None:
        result, _ = percentage_change(50, 50)
        assert result == 0.0

    def test_trace_shows_formula(self) -> None:
        _, trace = percentage_change(80, 100)
        assert any("old" in step for step in trace)
        assert any("new" in step for step in trace)


class TestRatio:
    def test_basic_ratio(self) -> None:
        result, trace = ratio(10, 4)
        assert result == 2.5
        assert len(trace) == 1

    def test_zero_denominator_raises(self) -> None:
        with pytest.raises(CalculationError, match="Denominator is zero"):
            ratio(10, 0)

    def test_ratio_less_than_one(self) -> None:
        result, _ = ratio(3, 7)
        assert 0 < result < 1
