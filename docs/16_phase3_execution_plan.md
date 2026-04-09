# GenUIWar — Phase 3 Execution Plan (Calculation Layer)

Generated: 2026-04-09
Branch: `feat/phase3-calculations`

---

## Scope

Phase 3 delivers the trusted calculation layer per `docs/05_build_phases.md`:
- Trusted calculator service
- Table operations
- Ratios and comparisons
- Calculation trace objects

## Out of scope

- Multi-agent orchestration (Phase 4)
- Answer generation (Phase 4+)
- Retrieval redesign
- Hidden arithmetic in prose

## Deliverables

### 1. Operations (`packages/calculators/operations.py`)
Pure functions: arithmetic, percentage_change, ratio, sum_values, group_total, compare.
Each returns `(result, trace_steps)`. No side effects.

### 2. Engine (`packages/calculators/engine.py`)
- `CalcRequest` model — operation name, inputs, evidence_refs
- `CalculationError` — raised for invalid inputs or denominators
- `CalculationEngine.execute()` — dispatches to operations, builds `CalculationResult`
- Standalone calcs use a request-scoped UUID as `run_id` (schema unchanged)

### 3. API (`apps/api/routes/calculations.py`)
- `POST /api/v1/calculations/execute`
- `GET /api/v1/calculations/{calculation_id}`

### 4. Tests (`tests/unit/`)
- Arithmetic, percentage change, aggregation, comparison
- Engine dispatch, trace completeness, invalid input, denominator safety
- API endpoints

## Schema decision

`CalculationResult.run_id` kept as required `UUID` (no schema change).
Standalone calculations use a generated execution-context UUID.

## Assumptions

| Assumption | Classification |
|-----------|---------------|
| No new Python dependencies | Fact — stdlib only |
| In-memory result store | Temporary — same pattern as Phase 1/2 |
| Operations are pure functions | Required by design |
| Request-scoped UUID for run_id | Temporary — until orchestration layer exists |

---

Status: Phase 3 execution plan
Use: bounded implementation guide for Phase 3 only
