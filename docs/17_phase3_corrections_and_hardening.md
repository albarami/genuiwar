# GenUIWar — Phase 3 Corrections and Hardening

Generated: 2026-04-09
Branch: `feat/phase3-calculations`

---

## What was wrong in the initial Phase 3 delivery

1. **Units support was missing.** Calculation results had no way to express input or output units. Percentage-change results had no `percent` unit. Traces did not indicate units.
2. **Dedicated trace endpoint was missing.** `docs/12_api_contract_overview.md` specifies "inspect calculation trace" as a distinct API operation, but only `execute` and `get-result` were implemented.
3. **Storage was raw dicts.** All in-memory stores were untyped `dict[UUID, ...]` in route modules — no abstraction, no path to Postgres.

## How units support was added

**Schema change (minimal):**
- Added `input_units: dict[str, str]` and `output_unit: str | None` to `CalculationResult`
- Added same fields to `CalcRequest`

**Engine behavior:**
- Percentage-change operations auto-infer `output_unit = "percent"`
- Callers can explicitly set `output_unit` (e.g., `"SAR"`) which overrides inference
- `input_units` are passed through for traceability
- Unit information is appended to the trace when present
- Operations with no meaningful unit leave `output_unit` as `None`

**No invented units.** Units are caller-supplied or inferred only for unambiguous operations.

## How the trace endpoint was added

- `GET /api/v1/calculations/{calculation_id}/trace`
- Returns typed `TraceResponse`: `calculation_id`, `operation`, `trace`, `output_unit`
- 404 if calculation not found
- Tested in `test_calc_api.py`

## What persistence enhancement was implemented

**Implemented: typed storage abstraction layer.**
- `packages/storage/base.py` — three ABCs: `ChunkRepository`, `BundleRepository`, `CalculationRepository`
- `packages/storage/memory.py` — in-memory implementations of all three
- API routes now use these typed repositories instead of raw dicts
- The `ChunkStore` in `packages/retrieval/store.py` remains as-is for now (it already implements the same interface shape)

**Not yet implemented: Postgres persistence.** The abstractions are ready. A Postgres implementation would subclass the same ABCs using SQLAlchemy. See `docs/18_persistence_and_retrieval_roadmap.md` for the migration path.

## What was deliberately deferred

- Postgres persistence (designed, not implemented)
- Vector/semantic retrieval (designed, not implemented)
- Full RAG orchestration (Phase 4)
- Trend calculations (can be added to operations.py later)

---

Status: Phase 3 corrections and hardening record
Use: traceability for what was fixed and why
