# GenUIWar — Phase 2 Execution Plan (Retrieval)

Generated: 2026-04-09
Branch: `feat/phase2-retrieval`

---

## Scope

Phase 2 delivers the retrieval foundation per `docs/05_build_phases.md`:
- Indexing (in-memory chunk store)
- Retrieval abstraction (keyword-based)
- Evidence bundles with citations
- Baseline retrieval API

## Out of scope

- Vector/semantic retrieval (future)
- Calculation layer (Phase 3)
- Multi-agent orchestration (Phase 4)
- Final-answer generation (Phase 4+)

## Deliverables

### 1. Schema addition (`packages/schemas/evidence.py`)
- `EvidenceBundle` — typed output of a retrieval operation

### 2. Retrieval core (`packages/retrieval/`)
- `base.py` — `BaseRetriever` ABC + `RetrievalFilters` model
- `store.py` — `ChunkStore` in-memory chunk index
- `local.py` — `LocalKeywordRetriever` keyword-matching implementation

### 3. Upload integration (`apps/api/routes/files.py`)
- Store parsed chunks in `ChunkStore` after upload

### 4. Retrieval API (`apps/api/routes/evidence.py`)
- `POST /api/v1/evidence/retrieve` — keyword retrieval
- `GET /api/v1/evidence/bundle/{bundle_id}` — fetch bundle
- `GET /api/v1/evidence/chunks/{file_id}` — chunks for a file

### 5. Tests (`tests/unit/`)
- Chunk store operations
- Keyword retrieval scoring and top-k
- Metadata filtering (file_id, content_type, sheet_name)
- Citation anchor preservation
- Mixed-file retrieval
- Empty/no-result cases
- Schema variation robustness

## Assumptions

| Assumption | Classification |
|-----------|---------------|
| In-memory ChunkStore (no persistence) | Temporary — same as Phase 1 file store |
| Keyword retrieval only (no vectors) | Per user instruction |
| EvidenceBundle added to existing evidence.py | Proposal |
| RetrievalFilters in retrieval package, not shared schemas | Proposal |
| No new Python dependencies | Fact — stdlib only |

---

Status: Phase 2 execution plan
Use: bounded implementation guide for Phase 2 only
