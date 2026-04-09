# packages/retrieval

Evidence search and bundle creation.

## Current state (Phase 2)

- `base.py` — `BaseRetriever` ABC and `RetrievalFilters` model
- `store.py` — `ChunkStore` in-memory chunk index (temporary; persistence deferred)
- `local.py` — `LocalKeywordRetriever` keyword-matching backend

Chunks are indexed after file upload. Retrieval returns `EvidenceBundle` objects
with citation anchors preserved from the original parse.

All final claims must map back to this layer.
