# GenUIWar — Phase 3 Corrections and Hardening

Updated: 2026-04-09 (second hardening pass)
Branch: `feat/phase3-calculations`

---

## What was wrong

1. **Units in trace incomplete.** Schema carried `input_units` and `output_unit`, but the engine only appended the output unit to the trace. Input units were never written to trace steps, making traces incomplete for auditing.
2. **Trace endpoint missing.** `docs/12_api_contract_overview.md` specifies "inspect calculation trace" as a distinct operation. Only execute and get-result existed.
3. **Storage bypass.** Routes imported the old `chunk_store` global from `packages/retrieval/store.py` directly, bypassing the typed `ChunkRepository` abstraction. The system was half on repositories (calculations, bundles) and half on a raw global (chunks). The `LocalKeywordRetriever` also took `ChunkStore` directly instead of `ChunkRepository`.

## How units-in-trace was fixed

- Engine now appends `input units: a: SAR, b: SAR` to trace when `input_units` is non-empty
- Engine appends `output unit: percent` to trace when `output_unit` is present
- When neither is provided, no unit lines appear in the trace
- Three new tests verify: input units in trace, output unit in trace, no fake units when absent

## How the trace endpoint was added

- `GET /api/v1/calculations/{calculation_id}/trace` returns `TraceResponse`
- `TraceResponse` is typed: `calculation_id`, `operation`, `trace`, `output_unit`
- Tests cover happy path, 404, and unit presence in trace response

## How storage abstraction was cleaned up

- Created `apps/api/dependencies.py` — centralized repository instances (`chunk_repo`, `bundle_repo`, `calc_repo`)
- All routes (`files.py`, `evidence.py`, `calculations.py`) now import from `dependencies.py`
- `LocalKeywordRetriever` now accepts `ChunkRepository` (the abstract interface) instead of `ChunkStore`
- No route imports `packages.retrieval.store` or `chunk_store` directly
- The old `packages/retrieval/store.py` is dead code — nothing imports it
- Tests updated: `test_chunk_store.py` tests `InMemoryChunkRepository`, `test_keyword_retriever.py` uses `InMemoryChunkRepository`, `test_evidence_bundle.py` uses `InMemoryChunkRepository`, `test_retrieval_api.py` clears via `chunk_repo` from dependencies

## What persistence was implemented

**Implemented:**
- Typed storage ABCs: `ChunkRepository`, `BundleRepository`, `CalculationRepository`
- In-memory implementations of all three
- All API routes use the typed repository abstraction
- Centralized dependency module for repository instantiation

**Documented only (not yet implemented):**
- Postgres-backed repositories (see `docs/18_persistence_and_retrieval_roadmap.md`)
- Full-text search indexing
- pgvector / semantic retrieval

## What was deliberately deferred

- Postgres persistence (abstractions ready, implementation deferred)
- SQLAlchemy models and Alembic migrations
- Vector retrieval / pgvector
- Hybrid retrieval
- Full retrieval redesign
- Multi-agent orchestration (Phase 4)

---

Status: Phase 3 corrections and hardening record (updated)
Use: traceability for what was fixed and why
