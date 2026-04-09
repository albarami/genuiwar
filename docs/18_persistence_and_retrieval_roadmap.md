# GenUIWar — Persistence and Retrieval Roadmap

Updated: 2026-04-09

---

## Why Postgres helps this system

The system currently uses in-memory stores for all data. Data is lost on restart.
For a ministry-grade system, persistence is required for:
- auditability (calculation traces, claim ledger entries must survive restarts)
- run reuse (evidence bundles must be queryable across sessions)
- evidence traceability (chunks must link back to source files permanently)

Postgres is the prescribed persistence backend per `.cursor/rules/00_architecture.mdc`.

## What should be persisted first

Recommended order follows data dependency:

1. **Calculation results** — claim ledger references `calculation_result_ids`
2. **Evidence bundles** — runs reference bundle IDs
3. **Evidence chunks** — bundles and claims reference chunk/evidence IDs
4. **File metadata** — chunks reference file IDs
5. **Runs and events** — needed for Phase 4 orchestration
6. **Claim ledger entries** — needed for Phase 4 adjudication
7. **Conversations and messages** — needed for Phase 5 UI

## Current state (implemented)

| Component | Storage | Abstraction |
|-----------|---------|-------------|
| Calculation results | In-memory (`InMemoryCalculationRepository`) | `CalculationRepository` ABC |
| Evidence bundles | In-memory (`InMemoryBundleRepository`) | `BundleRepository` ABC |
| Evidence chunks | In-memory (`InMemoryChunkRepository`) | `ChunkRepository` ABC |
| File metadata | In-memory dict in `files.py` | No abstraction yet |

All API routes use the typed repository interfaces via `apps/api/dependencies.py`.
To migrate to Postgres: implement the ABCs with SQLAlchemy and swap the imports.

## Exact recommended implementation order

1. **Set up Alembic** (already a dependency)
2. **Create SQLAlchemy models** for `CalculationResult`, `EvidenceChunk`, `EvidenceBundle`
3. **Create `PostgresCalculationRepository(CalculationRepository)`**
4. **Verify** existing tests still pass with the new implementation
5. **Repeat** for chunks and bundles
6. **Add indexing** for chunks:
   - `file_id` index (used by `get_by_file`)
   - `content_type` index (used by content_type filter)
   - GIN index on `citation_anchor` JSONB (for sheet_name, page, section lookups)
   - `tsvector` column + GIN index on `content` (for full-text search)
7. **Create `PostgresKeywordRetriever(BaseRetriever)`** using `ts_query`
8. **Add pgvector** when embedding infrastructure is ready

## How retrieval should evolve

### Current: Local keyword retrieval
- `LocalKeywordRetriever` scores by keyword token overlap
- Operates over `ChunkRepository.get_all()`
- Sufficient for Phase 2-3 development

### Next: Postgres full-text retrieval
- `tsvector` column on chunk content
- `ts_query` for ranked search
- `PostgresKeywordRetriever(BaseRetriever)` — same interface, better scoring

### Future: pgvector semantic retrieval
- Embedding column on chunk table
- `pgvector` extension for similarity search
- `PgVectorRetriever(BaseRetriever)`

### Future: Hybrid retrieval
- Combine keyword + vector scores
- `HybridRetriever(BaseRetriever)`

## Is pgvector recommended?

Yes. pgvector runs inside the same Postgres instance — no additional infrastructure.
It supports both exact and approximate nearest-neighbor search and integrates
naturally with Postgres full-text search for hybrid approaches.

## Is Azure AI Search still relevant?

Yes, as a later optional adapter per `docs/01_system_architecture.md`:
"adapters for later Azure Search / ministry connectors if needed."
It is not recommended as the primary path. Postgres + pgvector is simpler.

## Index design for chunk persistence

When chunks move to Postgres, the table should include:

| Column | Type | Index |
|--------|------|-------|
| chunk_id | UUID PK | Primary |
| file_id | UUID | B-tree |
| content | TEXT | GIN (tsvector) |
| content_type | VARCHAR | B-tree |
| citation_anchor | JSONB | GIN |
| metadata | JSONB | GIN (optional) |
| embedding | vector(3072) | HNSW (future) |
| created_at | TIMESTAMPTZ | B-tree |

---

Status: persistence and retrieval roadmap (updated)
Use: implementation guide for storage evolution
