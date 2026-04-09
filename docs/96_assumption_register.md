# GenUIWar — Assumption Register

Updated: 2026-04-08 (Correction pass 2)
Purpose: Document every assumption introduced during Phase 0 scaffold that was not explicitly prescribed in the controlling docs.

---

## Classification key

- **Required**: Explicitly prescribed by controlling docs or user rules.
- **Optional (proposal)**: Reasonable choice but not prescribed. Requires owner approval.
- **Premature**: Belongs to a later phase. Should not be in Phase 0.
- **Reverted**: Was present but has been removed.

---

## Assumptions

### 1. ARQ as worker queue library

- **What**: `arq` was added to `pyproject.toml` as the task queue for `apps/worker/`.
- **Doc basis**: `01_system_architecture.md` says "worker process for async jobs". No library is named.
- **Classification**: **Reverted (premature)**. Removed in correction pass 1.

### 2. Tailwind CSS v4

- **What**: `tailwindcss ^4` and `@tailwindcss/postcss ^4` were added to `apps/web/package.json`. `globals.css` used `@import "tailwindcss"`. `postcss.config.mjs` referenced `@tailwindcss/postcss`.
- **Doc basis**: No CSS framework is prescribed anywhere. `00_architecture.mdc` says "Next.js for frontend" only. CSS framework choice belongs to Phase 5 (Generative UI).
- **Classification**: **Reverted (premature)**. Removed in correction pass 2. Phase 0 frontend shell now uses plain CSS only. CSS framework decision deferred to Phase 5.

### 3. Next.js 15 (App Router)

- **What**: `next ^15.3` in `apps/web/package.json`. App Router structure (`src/app/`).
- **Doc basis**: `00_architecture.mdc` says "Next.js for frontend". No version specified. No routing paradigm specified.
- **Classification**: **Optional (proposal)**. Next.js 15 is the current stable release. App Router is the current recommended pattern. However, the version and routing model were chosen without explicit approval.

### 4. React 19

- **What**: `react ^19.1` and `react-dom ^19.1` in `apps/web/package.json`.
- **Doc basis**: Follows from Next.js 15 which requires React 19.
- **Classification**: **Required** — dependency of the chosen Next.js version.

### 5. `tests/unit/` directory

- **What**: Created `tests/unit/` and placed `test_schemas.py` there.
- **Doc basis**: The user's Phase D instructions requested `tests/integration` and `tests/e2e`. `06_repo_structure.md` shows only `tests/`. Neither mentions `tests/unit/`.
- **Classification**: **Optional (proposal)**. Standard Python convention but not requested.

### 6. pnpm as Node package manager

- **What**: pnpm installed globally, `pnpm-workspace.yaml` created.
- **Doc basis**: User explicitly requested `pnpm-workspace.yaml` in Phase C instructions.
- **Classification**: **Required**.

### 7. pnpm version constraint `>=9`

- **What**: `"pnpm": ">=9"` in root `package.json` engines field.
- **Doc basis**: Not specified. pnpm 10.33.0 was installed on the machine. The `>=9` constraint was chosen by the scaffold author.
- **Classification**: **Optional (proposal)**. The minimum was set to 9 rather than 10 for broader compatibility, but no doc prescribes this.

### 8. Node.js version constraint `>=20`

- **What**: `"node": ">=20"` in root `package.json` engines field.
- **Doc basis**: Not specified. Node.js v22.20.0 was available on the machine. `>=20` was chosen to accept the current LTS range.
- **Classification**: **Optional (proposal)**. No doc prescribes a minimum Node version.

### 9. Postgres 16 Alpine (Docker image version)

- **What**: `postgres:16-alpine` in `docker-compose.yml`.
- **Doc basis**: `00_architecture.mdc` says "Postgres for persistence". No version specified.
- **Classification**: **Optional (proposal)**.

### 10. Redis 7 Alpine (Docker image version)

- **What**: `redis:7-alpine` in `docker-compose.yml`.
- **Doc basis**: `.env.example` specifies `REDIS_URL` and `QUEUE_BACKEND=redis`. No version specified.
- **Classification**: **Optional (proposal)**.

### 11. structlog as logging library

- **What**: `structlog>=24.4` in `pyproject.toml`.
- **Doc basis**: `03_coding_standards.mdc` says "Log important run and adjudication events clearly." `.env.example` has `ENABLE_STRUCTURED_LOGGING=true`. No library is named.
- **Classification**: **Optional (proposal)**.

### 12. SQLAlchemy 2.x + psycopg + Alembic

- **What**: `sqlalchemy>=2.0`, `psycopg[binary]>=3.2`, `alembic>=1.14` in `pyproject.toml`.
- **Doc basis**: User rules say "SQLAlchemy" explicitly. `00_architecture.mdc` says "Postgres for persistence."
- **Classification**: **Required**.

### 13. setuptools as Python build backend

- **What**: `setuptools>=70` in `pyproject.toml` `[build-system]`.
- **Doc basis**: Not specified.
- **Classification**: **Optional (proposal)**. Standard default but alternatives (hatchling, flit) exist.

### 14. uvicorn as ASGI server

- **What**: `uvicorn[standard]>=0.34` in `pyproject.toml`.
- **Doc basis**: Not named explicitly. Follows from FastAPI which requires an ASGI server.
- **Classification**: **Required** — FastAPI needs an ASGI server; uvicorn is the standard pairing.

### 15. redis Python client

- **What**: `redis>=5.2` in `pyproject.toml`.
- **Doc basis**: `.env.example` has `REDIS_URL`, `QUEUE_BACKEND=redis`, `CACHE_BACKEND=redis`. A Python client is needed.
- **Classification**: **Required** — `.env.example` contract implies Redis connectivity.

### 16. TypeScript 5.8

- **What**: `typescript ^5.8` in `apps/web/package.json`.
- **Doc basis**: Not specified. Follows from Next.js 15 which uses TypeScript.
- **Classification**: **Optional (proposal)**. The specific minor version is a scaffold choice.

### 17. ESLint 9 + eslint-config-next

- **What**: `eslint ^9` and `eslint-config-next ^15.3` in `apps/web/package.json`.
- **Doc basis**: Not specified. Standard Next.js dev tooling.
- **Classification**: **Optional (proposal)**. Reasonable but not prescribed.

### 18. ruff lint rule selection

- **What**: Specific ruff rule sets selected: E, W, F, I, N, UP, B, SIM, T20, RUF.
- **Doc basis**: User rules say "Format and lint with ruff." Specific rules not prescribed.
- **Classification**: **Optional (proposal)**. The rule set is the scaffold author's selection.

### 19. mypy strict mode

- **What**: `strict = true` in `[tool.mypy]` section of `pyproject.toml`.
- **Doc basis**: User rules say "Type hints on all function signatures." Strict mode is not explicitly requested.
- **Classification**: **Optional (proposal)**. Strict mode enforces more than type hints on signatures. It is a stronger discipline than required.

### 20. Python line-length 100

- **What**: `line-length = 100` in `[tool.ruff]` section.
- **Doc basis**: Not specified. User rules don't prescribe a line length.
- **Classification**: **Optional (proposal)**. 100 is a common choice between 88 (ruff default) and 120.

### 21. `sse-starlette` (removed)

- **What**: Was in `pyproject.toml` for SSE streaming.
- **Doc basis**: SSE streaming is Phase 5.
- **Classification**: **Reverted (premature)**. Removed in correction pass 1.

### 22. `httpx` in main deps (removed, kept in dev)

- **What**: Was in main `pyproject.toml` dependencies. Kept in dev for test client.
- **Doc basis**: No runtime use in Phase 0.
- **Classification**: Main dep **reverted (premature)**. Dev dep **required** for testing.

### 23. `python-multipart` (removed)

- **What**: Was in `pyproject.toml` for multipart file upload.
- **Doc basis**: File upload is Phase 1.
- **Classification**: **Reverted (premature)**.

### 24. PostCSS (removed)

- **What**: `postcss ^8` was in `apps/web/package.json` devDependencies. `postcss.config.mjs` existed.
- **Doc basis**: Required only by Tailwind. Not needed without it.
- **Classification**: **Reverted** — removed along with Tailwind in correction pass 2.

---

## Summary table

| # | Assumption | Classification | Current status |
|---|-----------|---------------|----------------|
| 1 | ARQ | Premature | Reverted |
| 2 | Tailwind CSS v4 | Premature | **Reverted (pass 2)** |
| 3 | Next.js 15 App Router | Optional (proposal) | Present — needs approval |
| 4 | React 19 | Required (Next.js dep) | Present |
| 5 | tests/unit/ | Optional (proposal) | Present — needs approval |
| 6 | pnpm | Required (user requested) | Present |
| 7 | pnpm >=9 | Optional (proposal) | Present — needs approval |
| 8 | Node >=20 | Optional (proposal) | Present — needs approval |
| 9 | Postgres 16 Alpine | Optional (proposal) | Present — needs approval |
| 10 | Redis 7 Alpine | Optional (proposal) | Present — needs approval |
| 11 | structlog | Optional (proposal) | Present — needs approval |
| 12 | SQLAlchemy + psycopg + Alembic | Required (user rules) | Present |
| 13 | setuptools | Optional (proposal) | Present — needs approval |
| 14 | uvicorn | Required (FastAPI dep) | Present |
| 15 | redis client | Required (.env contract) | Present |
| 16 | TypeScript 5.8 | Optional (proposal) | Present — needs approval |
| 17 | ESLint 9 | Optional (proposal) | Present — needs approval |
| 18 | ruff rule selection | Optional (proposal) | Present — needs approval |
| 19 | mypy strict mode | Optional (proposal) | Present — needs approval |
| 20 | line-length 100 | Optional (proposal) | Present — needs approval |
| 21 | sse-starlette | Premature | Reverted |
| 22 | httpx (main dep) | Premature | Reverted (kept dev) |
| 23 | python-multipart | Premature | Reverted |
| 24 | PostCSS | Premature (Tailwind dep) | **Reverted (pass 2)** |
| 25 | `input_units` / `output_unit` on CalculationResult | Required (Phase 3 fix) | Present |
| 26 | Auto-inferred `percent` unit for percentage_change | Optional (proposal) | Present — needs approval |
| 27 | Storage ABCs in packages/storage/base.py | Required (persistence design) | Present |
| 28 | In-memory repository implementations | Temporary | Present — Postgres migration deferred |
| 29 | Request-scoped UUID as run_id for standalone calcs | Temporary | Present — until orchestration |
| 30 | pgvector recommended for future vector retrieval | Optional (proposal) | Documented only |
| 31 | reportlab as dev dependency for PDF fixtures | Optional (proposal) | Present — needs approval |
| 32 | Centralized `apps/api/dependencies.py` for repo instances | Required (clean architecture) | Present |
| 33 | `LocalKeywordRetriever` accepts `ChunkRepository` ABC | Required (storage cleanup) | Present |
| 34 | `packages/retrieval/store.py` was dead code | Fact | **Deleted** |
| 35 | SQLAlchemy ORM models in packages/storage/models.py | Required (Postgres persistence) | Present |
| 36 | Postgres repo implementations in packages/storage/postgres.py | Required (Postgres persistence) | Present |
| 37 | Alembic migration 001_initial_tables | Required (schema management) | Present |
| 38 | `RETRIEVAL_BACKEND` config selects in-memory vs Postgres | Required (backend selection) | Present |
| 39 | GIN index on citation_anchor JSONB | Required (retrieval performance) | Present in migration |
| 40 | alembic.ini at repo root | Required (Alembic convention) | Present |

**Items marked "proposal" require owner approval before they become approved decisions.**
**Items marked "reverted" or "deleted" are no longer in the codebase.**

---

Status: assumption register (updated Phase 3 final hardening)
Use: transparency record of all non-prescribed choices
