# GenUIWar — Persistence and Retrieval Roadmap

Generated: 2026-04-09

---

## Why Postgres should replace in-memory stores

The system currently uses in-memory dicts and lists for:
- file metadata (`_file_store` in files.py)
- evidence chunks (`ChunkStore` in retrieval/store.py)
- evidence bundles (`InMemoryBundleRepository`)
- calculation results (`InMemoryCalculationRepository`)

These are volatile — data is lost on restart. For a ministry-grade system,
persistence is required for auditability, run reuse, and evidence traceability.

Postgres is the prescribed persistence backend per `.cursor/rules/00_architecture.mdc`.

## What should be persisted first

Recommended migration order:

1. **Calculation results** — needed for claim ledger `calculation_result_ids` references
2. **Evidence chunks** — needed for claim ledger `evidence_refs` references
3. **Evidence bundles** — needed for run-to-bundle linkage
4. **File metadata** — needed for conversation-to-file relationships
5. **Runs and events** — needed for Phase 4 orchestration
6. **Claim ledger entries** — needed for Phase 4 adjudication
7. **Conversations and messages** — needed for Phase 5 UI

This order follows dependency: claims reference calculations and evidence,
runs reference bundles, etc.

## Storage abstraction (implemented)

`packages/storage/base.py` defines three abstract repositories:
- `ChunkRepository` — add, get_all, get_by_file, count, clear
- `BundleRepository` — save, get
- `CalculationRepository` — save, get

`packages/storage/memory.py` provides in-memory implementations.
API routes already use these typed abstractions.

To migrate to Postgres: implement the same ABCs using SQLAlchemy models
and swap the instantiation — no route code changes needed.

## How retrieval should evolve

### Current: Local keyword retrieval (Phase 2)
- `LocalKeywordRetriever` in `packages/retrieval/local.py`
- Tokenize query into keywords, score by overlap
- In-memory chunk store
- Sufficient for Phase 2-3 development

### Next: Postgres full-text retrieval
- Replace `ChunkStore` with a Postgres-backed `ChunkRepository`
- Use Postgres `tsvector` / `ts_query` for full-text search
- Keep the `BaseRetriever` interface unchanged
- Create `PostgresKeywordRetriever(BaseRetriever)`

### Future: pgvector semantic retrieval
- Add an embedding column to the chunk table
- Use `pgvector` extension for similarity search
- Create `PgVectorRetriever(BaseRetriever)`
- Embeddings generated via the Azure OpenAI embedding deployment

### Future: Hybrid retrieval
- Combine keyword + vector scores
- Create `HybridRetriever(BaseRetriever)` that merges results
- Configurable weighting between keyword and semantic

### Optional adapter: Azure AI Search
- Per `docs/01_system_architecture.md`: "adapters for later Azure Search"
- Create `AzureSearchRetriever(BaseRetriever)` if needed
- Uses Azure Search index instead of local Postgres
- Not recommended as the primary path; Postgres + pgvector is simpler

## Recommended: pgvector

pgvector is recommended over a separate vector DB because:
- It runs inside the same Postgres instance (no additional infrastructure)
- It is compatible with SQLAlchemy
- It supports both exact and approximate nearest-neighbor search
- It integrates naturally with the existing Postgres full-text search

## Chunk indexing evolution

| Phase | Indexing approach |
|-------|-----------------|
| Current | In-memory list, no indexing |
| Postgres FTS | `tsvector` column with GIN index on chunk content |
| pgvector | `vector` column with HNSW or IVFFlat index on embeddings |
| Hybrid | Both GIN and vector indexes on the same table |

## Metadata indexing

Evidence chunks have `metadata: dict[str, str]` and `citation_anchor` fields.
For efficient filtering:
- Index `file_id` (already used for get_by_file)
- Index `content_type` (used for content_type filter)
- Index `citation_anchor.sheet_name` (used for sheet_name filter)
- Consider JSONB index on `metadata` for schema-specific queries

## Bundle persistence

Evidence bundles should be persisted with:
- The bundle ID and query
- References to chunk IDs (not copies of chunks)
- The run ID that triggered the retrieval
- Timestamp

This avoids data duplication and allows bundle reconstruction.

## Exact recommended implementation order

1. Set up Alembic migrations (already a dependency)
2. Create SQLAlchemy models for `CalculationResult`
3. Create `PostgresCalculationRepository(CalculationRepository)`
4. Verify with existing tests (swap repository, tests should still pass)
5. Repeat for chunks and bundles
6. Add `tsvector` column and `PostgresKeywordRetriever`
7. Add pgvector when embedding infrastructure is ready

---

Status: persistence and retrieval roadmap
Use: implementation guide for storage evolution
