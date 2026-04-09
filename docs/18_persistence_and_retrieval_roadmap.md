# GenUIWar — Persistence and Retrieval Roadmap

Updated: 2026-04-09

---

## Why Postgres helps this system

Ministry-grade auditability requires that calculation traces, evidence chains,
and claim ledger entries survive restarts. In-memory stores lose data on any
restart. Postgres is prescribed by `.cursor/rules/00_architecture.mdc`.

## What should be persisted first

Order follows data dependency (claims reference calculations and evidence):

1. **Calculation results** — claim ledger references `calculation_result_ids`
2. **Evidence bundles** — runs reference bundle IDs
3. **Evidence chunks** — bundles and claims reference chunk/evidence IDs
4. **File metadata** — chunks reference file IDs
5. **Runs and events** — Phase 4 orchestration
6. **Claim ledger entries** — Phase 4 adjudication
7. **Conversations and messages** — Phase 5 UI

## Current state (implemented)

| Component | In-memory | Postgres | Migration |
|-----------|-----------|----------|-----------|
| Calculation results | `InMemoryCalculationRepository` | `PostgresCalculationRepository` | `001_initial_tables` |
| Evidence chunks | `InMemoryChunkRepository` | `PostgresChunkRepository` | `001_initial_tables` |
| Evidence bundles | `InMemoryBundleRepository` | `PostgresBundleRepository` | `001_initial_tables` |
| File metadata | raw dict in `files.py` | Not yet | — |

Backend selection: `RETRIEVAL_BACKEND=local` (in-memory, default) or `RETRIEVAL_BACKEND=postgres`.

## How to activate Postgres

1. `docker compose up -d` (starts Postgres on port 5432)
2. `alembic upgrade head` (applies migrations)
3. Set `RETRIEVAL_BACKEND=postgres` in `.env`

## Index design (implemented in migration 001)

| Table | Column | Index type | Purpose |
|-------|--------|-----------|---------|
| evidence_chunks | file_id | B-tree | get_by_file lookups |
| evidence_chunks | content_type | B-tree | content_type filter |
| evidence_chunks | citation_anchor | GIN (JSONB) | sheet_name, page, section lookups |

## Retrieval evolution roadmap

### Current: Local keyword retrieval (implemented)
- `LocalKeywordRetriever` scores by keyword token overlap
- Operates over `ChunkRepository.get_all()`
- Works with both in-memory and Postgres backends

### Next: Postgres full-text retrieval
- Add `tsvector` column to evidence_chunks (migration)
- Add GIN index on the tsvector column
- Create `PostgresKeywordRetriever(BaseRetriever)` using `ts_query`

### Future: pgvector semantic retrieval
- Add `vector(3072)` column to evidence_chunks
- Add HNSW index for approximate nearest-neighbor
- Create `PgVectorRetriever(BaseRetriever)`
- Embeddings via Azure OpenAI embedding deployment

### Future: Hybrid retrieval
- Combine keyword + vector scores
- Create `HybridRetriever(BaseRetriever)`

## Is pgvector recommended?

Yes. Runs inside the same Postgres instance. No additional infrastructure.
Supports exact and approximate nearest-neighbor search.

## Is Azure AI Search still relevant?

Yes, as a later optional adapter. Not recommended as the primary path.

---

Status: persistence and retrieval roadmap (final)
Use: implementation guide for storage evolution
