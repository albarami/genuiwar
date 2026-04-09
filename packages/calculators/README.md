# packages/calculators

Trusted numeric logic for the GenUIWar analytical system.

## Current state (Phase 3)

- `operations.py` — Pure functions: arithmetic, percentage_change, ratio, sum_values, group_total, compare
- `engine.py` — `CalculationEngine` dispatcher, `CalcRequest` model, `CalculationError`

Every calculation produces a typed `CalculationResult` with a full trace.
No trusted numeric statement may bypass this layer.
