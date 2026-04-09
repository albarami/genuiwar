# packages/storage

Storage adapters and persistence helpers.

## Current state (Phase 3 final)

- `base.py` — Abstract repository contracts: `ChunkRepository`, `BundleRepository`, `CalculationRepository`
- `memory.py` — In-memory implementations (default for local dev)
- `postgres.py` — Postgres implementations using SQLAlchemy
- `database.py` — SQLAlchemy engine and session factory
- `models.py` — ORM models for all three entity types
- `migrations/` — Alembic migration directory

## Backend selection

Set `RETRIEVAL_BACKEND` in `.env`:
- `local` (default) — in-memory repositories
- `postgres` — Postgres-backed repositories

## To activate Postgres

```bash
docker compose up -d
alembic upgrade head
# set RETRIEVAL_BACKEND=postgres in .env
```

See `docs/18_persistence_and_retrieval_roadmap.md` for the full migration plan.
