# GenUIWar — Assumption Register

Generated: 2026-04-08 (Correction pass)
Purpose: Document every assumption introduced during Phase 0 scaffold that was not explicitly prescribed in the controlling docs.

---

## Assumptions

### 1. ARQ as worker queue library

- **What**: `arq` was added to `pyproject.toml` as the task queue for `apps/worker/`.
- **Doc basis**: `01_system_architecture.md` says "worker process for async jobs". No library is named.
- **Status**: **Reverted (premature)**. Removed from Phase 0 dependencies. The worker skeleton (`apps/worker/main.py`) exists as a plain Python entry point with no queue dependency. The queue library choice should be made when Phase 1 worker jobs are implemented.

### 2. Tailwind CSS v4

- **What**: `tailwindcss ^4` and `@tailwindcss/postcss ^4` added to `apps/web/package.json`. `globals.css` uses `@import "tailwindcss"` (v4 syntax).
- **Doc basis**: `04_ui_ux_contract.md` specifies the UI must render structured blocks, drawers, and live streams. No CSS framework is prescribed. `00_architecture.mdc` says "Next.js for frontend" only.
- **Classification**: **Optional — proposal, not approved**. Tailwind is a reasonable default for component-heavy UIs, but it was not requested. The owner may prefer a different styling approach.
- **Action**: Kept in scaffold because removing it would leave the frontend without any styling mechanism, making the shell non-functional. Documented as a proposal.

### 3. Next.js 15 (App Router)

- **What**: `next ^15.3` in `apps/web/package.json`. App Router structure (`src/app/`).
- **Doc basis**: `00_architecture.mdc` says "Next.js for frontend". No version specified. No routing paradigm specified.
- **Classification**: **Optional — reasonable default**. Next.js 15 is the current stable release. App Router is the recommended pattern for new Next.js projects. However, the version and routing model were chosen without explicit approval.
- **Action**: Kept. The docs say "Next.js" and this is the current Next.js. Documented as a proposal.

### 4. React 19

- **What**: `react ^19.1` and `react-dom ^19.1` in `apps/web/package.json`.
- **Doc basis**: Not specified. Follows from Next.js 15 which requires React 19.
- **Classification**: **Required** — Next.js 15 depends on React 19. Not a free choice.
- **Action**: No change needed.

### 5. `tests/unit/` directory

- **What**: Created `tests/unit/` and placed `test_schemas.py` there.
- **Doc basis**: The user's Phase D instructions requested `tests/integration` and `tests/e2e`. The `06_repo_structure.md` shows only `tests/`. Neither document mentions `tests/unit/`.
- **Classification**: **Optional — reasonable addition**. The schema tests need a home. `tests/unit/` is standard Python project structure.
- **Action**: Kept. The alternative would be placing tests directly in `tests/` root, which is less organized.

### 6. pnpm as Node package manager

- **What**: pnpm installed globally, `pnpm-workspace.yaml` created, root `package.json` uses pnpm filter commands.
- **Doc basis**: `00_project_setup_checklist.md` says "package managers chosen" as a pre-coding requirement. `00_architecture.mdc` does not specify a Node package manager. The user's Phase C instructions explicitly requested `pnpm-workspace.yaml`.
- **Classification**: **Required** — the user explicitly requested pnpm workspace configuration.
- **Action**: No change needed.

### 7. Postgres 16 Alpine (Docker image version)

- **What**: `postgres:16-alpine` in `docker-compose.yml`.
- **Doc basis**: `00_architecture.mdc` says "Postgres for persistence". No version specified.
- **Classification**: **Optional — reasonable default**. Postgres 16 is the current stable. Alpine reduces image size.
- **Action**: Kept. Documented as a proposal.

### 8. Redis 7 Alpine (Docker image version)

- **What**: `redis:7-alpine` in `docker-compose.yml`.
- **Doc basis**: `.env.example` specifies `REDIS_URL` and `QUEUE_BACKEND=redis`. No version specified.
- **Classification**: **Optional — reasonable default**. Redis 7 is the current stable.
- **Action**: Kept. Documented as a proposal.

### 9. structlog as logging library

- **What**: `structlog>=24.4` in `pyproject.toml`.
- **Doc basis**: `03_coding_standards.mdc` says "Log important run and adjudication events clearly." `.env.example` has `ENABLE_STRUCTURED_LOGGING=true`.
- **Classification**: **Optional — reasonable default**. The `.env.example` names "structured logging" as a feature, but does not name a library. structlog is the standard Python structured logging library.
- **Action**: Kept. Documented as a proposal.

### 10. SQLAlchemy 2.x + psycopg + Alembic

- **What**: `sqlalchemy>=2.0`, `psycopg[binary]>=3.2`, `alembic>=1.14` in `pyproject.toml`.
- **Doc basis**: User rules say "SQLAlchemy" explicitly. `00_architecture.mdc` says "Postgres for persistence." Alembic is the standard migration tool for SQLAlchemy.
- **Classification**: **Required** — user rules prescribe SQLAlchemy. Alembic follows from SQLAlchemy + Postgres.
- **Action**: No change needed.

### 11. setuptools as build backend

- **What**: `setuptools>=70` as build-system in `pyproject.toml`.
- **Doc basis**: Not specified. The user rules say "Python 3.11+, Pydantic v2, FastAPI, SQLAlchemy" but do not name a build tool.
- **Classification**: **Optional — standard default**. setuptools is the most widely compatible Python build backend.
- **Action**: Kept. Documented as a proposal.

### 12. `sse-starlette` (removed)

- **What**: Was in `pyproject.toml` for SSE streaming.
- **Doc basis**: `.env.example` has `STREAM_TRANSPORT=sse`. However, SSE streaming is Phase 5 (Generative UI).
- **Classification**: **Premature**.
- **Action**: **Reverted** — removed in Correction D.

### 13. `httpx` (removed from main deps, kept in dev)

- **What**: Was in main dependencies. Also in dev dependencies.
- **Doc basis**: No runtime use in Phase 0. Useful as pytest test client.
- **Classification**: Main dep was **premature**. Dev dep is **required** for testing.
- **Action**: **Reverted** from main deps. Kept in dev deps only.

### 14. `python-multipart` (removed)

- **What**: Was in `pyproject.toml` for multipart file upload.
- **Doc basis**: File upload is Phase 1.
- **Classification**: **Premature**.
- **Action**: **Reverted** — removed in Correction D.

---

## Summary

| # | Assumption | Classification | Action |
|---|-----------|---------------|--------|
| 1 | ARQ | Premature | **Reverted** |
| 2 | Tailwind CSS v4 | Optional (proposal) | Kept, documented |
| 3 | Next.js 15 App Router | Optional (proposal) | Kept, documented |
| 4 | React 19 | Required (Next.js dep) | No change |
| 5 | tests/unit/ | Optional (reasonable) | Kept, documented |
| 6 | pnpm | Required (user requested) | No change |
| 7 | Postgres 16 Alpine | Optional (proposal) | Kept, documented |
| 8 | Redis 7 Alpine | Optional (proposal) | Kept, documented |
| 9 | structlog | Optional (proposal) | Kept, documented |
| 10 | SQLAlchemy + psycopg + Alembic | Required (user rules) | No change |
| 11 | setuptools | Optional (standard) | Kept, documented |
| 12 | sse-starlette | Premature | **Reverted** |
| 13 | httpx (main dep) | Premature | **Reverted** (kept in dev) |
| 14 | python-multipart | Premature | **Reverted** |

**Items marked "proposal" require owner approval before they become approved decisions.**

---

Status: assumption register
Use: transparency record of non-prescribed choices
