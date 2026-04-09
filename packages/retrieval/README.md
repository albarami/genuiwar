# packages/retrieval

Evidence search and bundle creation.

## Current state (Phase 3 hardened)

- `base.py` — `BaseRetriever` ABC and `RetrievalFilters` model
- `local.py` — `LocalKeywordRetriever` operating over `ChunkRepository` abstraction
- `store.py` — Legacy `ChunkStore` (dead code; superseded by `packages/storage/`)

Chunks are persisted via `ChunkRepository` (currently in-memory).
Retrieval returns `EvidenceBundle` objects with citation anchors preserved.

All final claims must map back to this layer.
