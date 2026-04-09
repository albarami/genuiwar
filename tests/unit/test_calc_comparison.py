"""Tests for compare operation."""

from packages.calculators.operations import compare


class TestCompare:
    def test_a_greater(self) -> None:
        result, trace = compare(100, 80)
        assert result["difference"] == 20
        assert result["direction"] == "a > b"
        assert result["percentage_difference"] == 25.0
        assert len(trace) >= 3

    def test_b_greater(self) -> None:
        result, _ = compare(50, 100)
        assert result["difference"] == -50
        assert result["direction"] == "a < b"

    def test_equal(self) -> None:
        result, _ = compare(42, 42)
        assert result["difference"] == 0
        assert result["direction"] == "a == b"

    def test_b_zero_no_percentage(self) -> None:
        result, trace = compare(10, 0)
        assert result["percentage_difference"] is None
        assert any("undefined" in step for step in trace)

    def test_negative_values(self) -> None:
        result, _ = compare(-5, -10)
        assert result["difference"] == 5
        assert result["direction"] == "a > b"
