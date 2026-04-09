# GenUIWar — Phase 3 Corrections and Hardening

Updated: 2026-04-09 (final hardening pass)
Branch: `feat/phase3-calculations`

---

## What was wrong

1. **Units in trace incomplete.** Input units were never written to trace steps.
2. **Trace endpoint missing.** Only execute and get-result existed.
3. **Storage bypass.** Routes imported a global `chunk_store` directly, bypassing the repository abstraction. The `LocalKeywordRetriever` took the concrete `ChunkStore` class instead of the `ChunkRepository` ABC.
4. **No Postgres persistence.** All storage was in-memory with no migration path implemented.
5. **Dead code.** `packages/retrieval/store.py` was superseded but not removed.

## How units-in-trace was fixed

- Engine appends `input units: a: SAR, b: SAR` when `input_units` is non-empty
- Engine appends `output unit: percent` when `output_unit` is present
- No unit lines appear when neither is provided
- Tests verify all three cases

## How storage abstraction was cleaned up

- Created `apps/api/dependencies.py` — centralized repository instances
- All routes import from `dependencies.py`, not from retrieval internals
- `LocalKeywordRetriever` accepts `ChunkRepository` ABC
- `packages/retrieval/store.py` deleted (dead code)
- Tests use `InMemoryChunkRepository` from `packages/storage`

## What Postgres persistence was implemented

**Implemented:**
- SQLAlchemy ORM models: `CalculationResultRow`, `EvidenceChunkRow`, `EvidenceBundleRow`
- Postgres repository implementations: `PostgresCalculationRepository`, `PostgresChunkRepository`, `PostgresBundleRepository`
- Database engine/session module: `packages/storage/database.py`
- Alembic initialized with migration directory
- Initial migration `001_initial_tables.py` with:
  - `calculation_results` table
  - `evidence_chunks` table with B-tree indexes on `file_id` and `content_type`, GIN index on `citation_anchor`
  - `evidence_bundles` table
- Repository selection mechanism in `dependencies.py`: reads `RETRIEVAL_BACKEND` config, creates Postgres or in-memory repos
- Default remains in-memory (`RETRIEVAL_BACKEND=local`)

**To activate Postgres:**
1. Run `docker compose up -d` (Postgres on port 5432)
2. Run `alembic upgrade head`
3. Set `RETRIEVAL_BACKEND=postgres` in `.env`

## What was intentionally deferred

- Postgres full-text search (`tsvector` column + `ts_query` retriever)
- pgvector / semantic retrieval
- Hybrid retrieval
- Multi-agent orchestration (Phase 4)

---

Status: Phase 3 corrections and hardening record (final)
Use: traceability for what was fixed and why
