# packages/retrieval

Evidence search and bundle creation.

## Current state (Phase 3 final)

- `base.py` — `BaseRetriever` ABC and `RetrievalFilters` model
- `local.py` — `LocalKeywordRetriever` operating over `ChunkRepository` abstraction

Chunks are persisted via `ChunkRepository` (in-memory or Postgres).
Retrieval returns `EvidenceBundle` objects with citation anchors preserved.

All final claims must map back to this layer.
