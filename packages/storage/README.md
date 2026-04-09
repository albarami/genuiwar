# packages/storage

Storage adapters and persistence helpers.

## Current state (Phase 3 hardening)

- `base.py` — Abstract repository contracts: `ChunkRepository`, `BundleRepository`, `CalculationRepository`
- `memory.py` — In-memory implementations (temporary; Postgres migration path documented)

API routes use these typed abstractions. To migrate to Postgres: implement
the same ABCs with SQLAlchemy and swap the instantiation.

See `docs/18_persistence_and_retrieval_roadmap.md` for the full migration plan.
