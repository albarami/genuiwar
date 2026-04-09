"""Pure calculation operations — each returns (result, trace_steps)."""

from typing import Any


class CalculationError(Exception):
    """Raised when a calculation cannot be performed safely."""

    def __init__(self, operation: str, reason: str) -> None:
        self.operation = operation
        self.reason = reason
        super().__init__(f"Calculation error in {operation}: {reason}")


def arithmetic(a: float, b: float, op: str) -> tuple[float, list[str]]:
    """Basic arithmetic: add, subtract, multiply, divide."""
    ops = {
        "add": (a + b, f"{a} + {b} = {a + b}"),
        "subtract": (a - b, f"{a} - {b} = {a - b}"),
        "multiply": (a * b, f"{a} * {b} = {a * b}"),
    }
    if op == "divide":
        if b == 0:
            raise CalculationError("divide", "Division by zero")
        result = a / b
        return result, [f"{a} / {b} = {result}"]

    if op not in ops:
        raise CalculationError("arithmetic", f"Unknown operator: {op}")

    result, step = ops[op]
    return result, [step]


def percentage_change(old: float, new: float) -> tuple[float, list[str]]:
    """Percentage change from old to new value."""
    if old == 0:
        raise CalculationError(
            "percentage_change",
            "Cannot compute percentage change from zero base",
        )
    change = (new - old) / old * 100
    trace = [
        f"old = {old}, new = {new}",
        "change = (new - old) / old * 100",
        f"change = ({new} - {old}) / {old} * 100 = {change}",
    ]
    return change, trace


def ratio(numerator: float, denominator: float) -> tuple[float, list[str]]:
    """Safe division returning a ratio."""
    if denominator == 0:
        raise CalculationError("ratio", "Denominator is zero")
    result = numerator / denominator
    return result, [f"{numerator} / {denominator} = {result}"]


def sum_values(values: list[float]) -> tuple[float, list[str]]:
    """Sum a list of numeric values."""
    if not values:
        return 0.0, ["sum([]) = 0"]
    total = sum(values)
    return total, [f"sum({values}) = {total}"]


def group_total(
    rows: list[dict[str, Any]],
    group_key: str,
    value_key: str,
) -> tuple[dict[str, float], list[str]]:
    """Group rows by a key and sum the value column per group."""
    if not rows:
        return {}, ["No rows to group"]

    groups: dict[str, float] = {}
    trace: list[str] = [f"grouping by '{group_key}', summing '{value_key}'"]

    for row in rows:
        gk = str(row.get(group_key, "unknown"))
        raw = row.get(value_key)
        try:
            val = float(raw)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        groups[gk] = groups.get(gk, 0.0) + val

    for group, total in sorted(groups.items()):
        trace.append(f"  {group}: {total}")

    return groups, trace


def compare(a: float, b: float) -> tuple[dict[str, Any], list[str]]:
    """Compare two values: difference, percentage difference, direction."""
    diff = a - b
    trace = [f"a = {a}, b = {b}", f"difference = {a} - {b} = {diff}"]

    pct_diff: float | None = None
    if b != 0:
        pct_diff = diff / b * 100
        trace.append(f"percentage difference = {diff} / {b} * 100 = {pct_diff}")
    else:
        trace.append("percentage difference: undefined (b is zero)")

    if a > b:
        direction = "a > b"
    elif a < b:
        direction = "a < b"
    else:
        direction = "a == b"
    trace.append(f"direction: {direction}")

    return {
        "difference": diff,
        "percentage_difference": pct_diff,
        "direction": direction,
    }, trace
