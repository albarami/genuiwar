"""Tests for sum_values and group_total aggregation operations."""

from packages.calculators.operations import group_total, sum_values


class TestSumValues:
    def test_basic_sum(self) -> None:
        result, trace = sum_values([10, 20, 30])
        assert result == 60
        assert len(trace) >= 1

    def test_empty_list(self) -> None:
        result, trace = sum_values([])
        assert result == 0.0
        assert "0" in trace[0]

    def test_single_value(self) -> None:
        result, _ = sum_values([42])
        assert result == 42

    def test_negative_values(self) -> None:
        result, _ = sum_values([10, -5, 3])
        assert result == 8


class TestGroupTotal:
    def test_basic_grouping(self) -> None:
        rows = [
            {"dept": "IT", "salary": 25000},
            {"dept": "HR", "salary": 22000},
            {"dept": "IT", "salary": 26000},
            {"dept": "HR", "salary": 21000},
        ]
        result, trace = group_total(rows, "dept", "salary")
        assert result["IT"] == 51000
        assert result["HR"] == 43000
        assert len(trace) >= 3

    def test_empty_rows(self) -> None:
        result, trace = group_total([], "dept", "salary")
        assert result == {}
        assert "No rows" in trace[0]

    def test_missing_value_key_skipped(self) -> None:
        rows = [
            {"dept": "IT", "salary": 25000},
            {"dept": "IT"},
        ]
        result, _ = group_total(rows, "dept", "salary")
        assert result["IT"] == 25000

    def test_non_numeric_value_skipped(self) -> None:
        rows = [
            {"dept": "IT", "salary": "not_a_number"},
            {"dept": "IT", "salary": 10000},
        ]
        result, _ = group_total(rows, "dept", "salary")
        assert result["IT"] == 10000

    def test_trace_shows_group_breakdown(self) -> None:
        rows = [
            {"dept": "A", "val": 10},
            {"dept": "B", "val": 20},
        ]
        _, trace = group_total(rows, "dept", "val")
        assert any("A:" in step for step in trace)
        assert any("B:" in step for step in trace)
