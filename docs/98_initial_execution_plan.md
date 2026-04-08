# GenUIWar — Initial Execution Plan (Phase 0 + Phase 1)

Generated: 2026-04-08
Scope: Phase 0 (Foundation) and Phase 1 (File Ingestion) only

---

## Phase 0 — Foundation

### 0.1 Repository and Environment Setup
- [x] Read and understand all docs, rules, AGENTS.md
- [ ] Initialize git repository
- [ ] Add remote origin `https://github.com/albarami/genuiwar`
- [ ] Create `.gitignore` (Python, Node, env files, data dirs, IDE)
- [ ] Create `pyproject.toml` with Python 3.11+, FastAPI, Pydantic v2, ruff, pytest
- [ ] Create root `package.json` for monorepo
- [ ] Install and configure pnpm; create `pnpm-workspace.yaml`
- [ ] Create `docker-compose.yml` (Postgres, Redis)
- [ ] Create `Makefile` for common dev tasks
- [ ] Create `.python-version` file (3.11)
- [ ] Preserve `.env.example` as environment contract

### 0.2 Repository Skeleton
Create the full folder structure per `06_repo_structure.md`:

```
apps/api/          — FastAPI backend
apps/web/          — Next.js frontend
apps/worker/       — Background job runner
packages/schemas/  — Typed shared contracts
packages/orchestration/
packages/agents/
packages/parsers/
packages/retrieval/
packages/calculators/
packages/governance/
packages/storage/
packages/prompts/
packages/evaluation/
packages/synthetic_data/
packages/shared/
infra/docker/
infra/scripts/
infra/deployment/
tests/integration/
tests/e2e/
```

Each directory gets a minimal `__init__.py` (Python packages) or `package.json` (Node packages) plus a brief `README.md` stating purpose and boundaries.

### 0.3 Shared Typed Schemas
Create initial Pydantic v2 models in `packages/schemas/`:
- `Conversation`
- `Message`
- `FileDocument`
- `EvidenceChunk`
- `Run` (with RunCategory, RunMode, RunStatus enums)
- `RunEvent` (with EventGroup enum)
- `ClaimLedgerEntry` (with ClaimType, SupportStatus, ConfidenceGrade, Materiality, AdjudicationStatus enums)
- `CalculationResult`
- `ClarificationRequest`

### 0.4 Configuration
- Config loading via Pydantic `BaseSettings` in `packages/shared/`
- All config from environment variables per `.env.example` contract
- No hardcoded values

### 0.5 Backend Bootstrap
- Minimal FastAPI app in `apps/api/` with health check endpoint
- CORS middleware
- Basic project structure (routes, dependencies, main)
- No business logic yet

### 0.6 Frontend Bootstrap
- Minimal Next.js app in `apps/web/`
- App Router structure (proposal — see `docs/96_assumption_register.md`)
- Plain CSS only — no CSS framework in Phase 0
- No UI features yet — just the shell
- CSS framework decision deferred to Phase 5 (Generative UI)

### 0.7 Worker Bootstrap
- Minimal worker entry point in `apps/worker/`
- No job processing yet — just the shell

### 0.8 Tests Foundation
- pytest configuration
- Test directory structure mirroring packages
- At least one smoke test for schema validation

---

## Phase 1 — File Ingestion

### 1.1 File Upload Endpoint
- `POST /api/v1/files/upload` accepting multipart files
- File metadata creation and persistence
- Storage to local filesystem (per `LOCAL_STORAGE_ROOT` config)
- File type validation (DOCX, PDF, PPTX, XLSX, CSV)

### 1.2 Parser Contracts
- Abstract parser interface in `packages/parsers/`
- Parser registry pattern (file type → parser)
- Normalized output contract: list of evidence chunks with citation anchors

### 1.3 Parser Implementations (Initial)
- DOCX parser (python-docx)
- PDF parser (PyMuPDF or pdfplumber)
- PPTX parser (python-pptx)
- XLSX parser (openpyxl)
- CSV parser (stdlib csv + pandas for structured tables)

Each parser produces:
- Normalized text blocks
- Table structures (where applicable)
- Citation anchors (file, page/section, position)
- File metadata object

### 1.4 Evidence Object Generation
- `EvidenceChunk` creation from parsed output
- Citation anchor attachment
- Chunk ID generation
- Structural ambiguity detection (flag for clarification triggers)

### 1.5 Tests for Phase 1
- Parser contract tests (each parser implements the interface correctly)
- Evidence chunk creation tests
- Citation anchor tests
- File upload endpoint integration test
- Edge cases: empty files, malformed files, unsupported types

### 1.6 Synthetic Test Files
- Create minimal synthetic files in `packages/synthetic_data/`
- At least one clean and one messy variant per file type
- Used for parser testing

---

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Python version | 3.11 | Matches available runtime; required by user rules |
| Backend framework | FastAPI | Per architecture docs |
| Frontend framework | Next.js (App Router) | Per architecture docs |
| ORM | SQLAlchemy 2.x | Per user rules |
| Schema validation | Pydantic v2 | Per user rules |
| Package manager (Python) | pip + pyproject.toml | Standard; venv-based |
| Package manager (Node) | pnpm | Monorepo-friendly; per workspace docs |
| Database | Postgres (via Docker) | Per architecture docs |
| Cache/Queue | Redis (via Docker) | Per architecture docs |
| Linting/Formatting | ruff | Per user rules |
| Testing | pytest | Per user rules |
| Task queue (worker) | To be decided in Phase 1 | Docs say "worker process" but prescribe no library |
| Local retrieval | To be decided in Phase 2 | pgvector or FAISS; not needed yet |

---

## Risks for Phase 0-1

| Risk | Mitigation |
|------|-----------|
| `.env` may contain secrets | `.gitignore` blocks `.env`; agents must never read it |
| pnpm not installed | Install globally via npm |
| ruff not installed | Install via pip |
| Schema evolution | Schemas are versioned and typed; easy to extend |
| Parser quality varies by file type | Abstract interface allows per-type quality iteration |

---

## Out of Scope (Explicitly Deferred)

- Multi-agent orchestration (Phase 4)
- Retrieval and indexing (Phase 2)
- Calculation layer (Phase 3)
- Generative UI features (Phase 5)
- Evaluation and red teaming (Phase 6)
- Azure OpenAI integration (adapter shell only in Phase 0)
- Production authentication
- Production deployment

---

Status: initial execution plan
Use: bounded implementation guide for Phase 0 and Phase 1 only
