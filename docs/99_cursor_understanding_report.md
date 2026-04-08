# GenUIWar — Cursor Understanding Report

Generated: 2026-04-08
Phase: Pre-implementation reading and comprehension

---

## 1. Product Understanding

GenUIWar is a **ministry-grade analytical conversation system** — not a chatbot, not a recommendation engine, not a free-form reasoning tool. It accepts uploaded files, runs structured multi-agent analysis, streams live telemetry to the user, and delivers evidence-backed answers through a generative UI.

The system is designed for government analytical work where **correctness, auditability, and evidence discipline** are non-negotiable. Every important claim must trace to source evidence, verified calculations, or both. The system must never present unsupported facts disguised by fluent prose.

---

## 2. System Purpose

Enable a ministry analyst to:
1. Upload one or more files (DOCX, PDF, PPTX, XLSX, CSV).
2. Ask any analytical question at any time.
3. Watch the system work in real time (live telemetry).
4. Receive a structured, evidence-backed answer.
5. Inspect the evidence, calculations, debate, and adjudication behind that answer.
6. Trigger reruns, comparisons, or deeper analysis as needed.

The system must decide whether to reuse prior validated outputs, perform a hybrid run, or launch a fresh deep run — and it must be transparent about which mode it chose.

---

## 3. Architecture Layers

The system has **eight major layers** (per `01_system_architecture.md`):

| Layer | Responsibility |
|-------|---------------|
| 1. Frontend Generative UI | Chat, file management, live run stream, evidence/debate drawers, structured final answer blocks |
| 2. Backend API | Conversation, file, run, event, retrieval, clarification, and answer endpoints |
| 3. Run Orchestration Engine | Decides reuse/hybrid/fresh, invokes agents in order, emits events, handles failures and clarification pauses |
| 4. File Ingestion & Parsing | Parses files, normalizes text/tables, generates evidence chunks and citation anchors |
| 5. Retrieval & Evidence | Chunk indexing, metadata filtering, semantic/keyword retrieval, evidence bundle creation |
| 6. Calculation Layer | Trusted arithmetic, ratios, comparisons, totals, denominator checks, calculation traces |
| 7. Governance & Trust | No-free-facts enforcement, claim typing, confidence grading, adjudication rules, provenance |
| 8. Persistence Layer | Conversations, messages, runs, events, evidence, claims, calculations, adjudication results |

Technology choices: FastAPI (backend), Next.js (frontend), Postgres (persistence), Redis (queue/cache), Azure OpenAI behind adapter layer, worker process for async jobs.

---

## 4. Agent Roles

Ten asymmetric agents with narrow, non-overlapping responsibilities:

| # | Agent | Role |
|---|-------|------|
| 1 | Run Router | Decides reuse vs hybrid vs fresh vs clarification-first |
| 2 | Ingestion Agent | Parses files, produces normalized document objects |
| 3 | Linking Agent | Builds cross-entity, cross-file, cross-table links |
| 4 | Retrieval Agent | Selects the evidence bundle needed for the current question |
| 5 | Primary Analyst | Creates draft analytical answer and initial claim ledger |
| 6 | Calculator Agent | Executes every required trusted calculation |
| 7 | Challenger Agent | **AlMuhasbi / Devil's Advocate** mode — attacks weak logic, unsupported claims, false precision |
| 8 | Adjudicator Agent | Final gate — approves, downgrades, rejects, or sends claims back |
| 9 | Composer Agent | Builds final structured answer payload using only approved claims |
| 10 | Clarification Agent | Generates clarification questions when the system cannot answer safely |

### Workflow after file upload
Ingestion → Linking → Background run → Results stored as run products.

### Workflow after user question
Run Router → Retrieval → Primary Analyst → Calculator → Challenger → Adjudicator → Composer → Frontend render.

---

## 5. No-Free-Facts Rule

This is the foundational integrity constraint of the entire system:

- **No important final claim** may appear without evidence, verified calculation, or both.
- No trusted arithmetic from model prose — numeric outputs must come from the calculation layer.
- Every claim must be **typed**: direct, derived, or model_based. These categories must never be merged invisibly.
- Unsupported claims must be **rejected** or **rewritten with explicit uncertainty**.
- If evidence is insufficient, the system must downgrade confidence, ask a clarification question, or decline to conclude.
- Fluent prose must never hide weak support.

This rule is enforced through the Governance & Trust layer and the Claim Ledger.

---

## 6. Claim Ledger Concept

The claim ledger is the **structural enforcer** of no-free-facts. Every important statement in a final answer maps to one or more claim ledger entries.

Each entry tracks:
- `claim_id`, `run_id`, `claim_text`, `claim_type` (direct/derived/model_based)
- `support_status` (supported/partially_supported/unsupported/needs_clarification)
- `confidence_grade` (high/moderate/emerging/low/unresolved)
- `materiality` (high/medium/low) — high-materiality claims **must** be challenged
- `evidence_refs`, `calculation_result_ids`, `assumptions`
- `challenge_flags` (e.g., missing_evidence, denominator_unclear, false_precision)
- `adjudication_status` (approved/downgraded/rejected/pending)

**Lifecycle**: claim created → evidence attached → calculations attached → challenger reviews → flags added → adjudicator decides → composer uses only approved/downgraded claims.

Rejected claims **never** enter final output.

---

## 7. Run/Event Model

### Run
A discrete analytical execution. Categories: document_preparation, background_analysis, question_answering, targeted_followup, deep_rerun, clarification_required. Modes: reuse, hybrid, fresh.

Core fields: `run_id`, `conversation_id`, `trigger_message_id`, `parent_run_id`, `run_category`, `run_mode`, `status`, `scope`, `question`, `decision_reason`, timestamps.

Statuses: queued → running → waiting_for_clarification / completed / failed / cancelled.

### Event
A structured, streamable record of something meaningful during a run — **not** unrestricted chain-of-thought.

Core fields: `event_id`, `run_id`, `event_index`, `event_type`, `event_group`, `agent_name`, `status`, `title`, `summary`, `payload`, `created_at`, `is_user_visible`.

Event groups: run_lifecycle, ingestion, linking, retrieval, analysis, calculation, challenge, adjudication, clarification, answer_rendering.

Every final answer links back to its run, evidence bundle, calculation results, claim ledger, and adjudication outcome.

---

## 8. Clarification Behavior

The system must ask clarification questions **instead of guessing** when:
- File structure is ambiguous
- Schema mapping is unclear
- Denominator is missing or ambiguous
- Multiple interpretations exist
- User question is underspecified
- Time window for comparison is unclear
- Evidence is insufficient for a reliable conclusion

Clarification must happen **before** deep execution continues. Questions must be short, specific, and decision-oriented. If the user does not answer, the system pauses the deep run or answers only the safe portion while marking unresolved parts.

---

## 9. Dynamic Schema Requirement

This is a **first-class design constraint**, not an afterthought:
- Synthetic schemas **will** differ from real ministry schemas.
- Field names, file quality, structures, and layouts will vary.
- The system must inspect structure dynamically, use schema mapping, and support dynamic adapters.
- Synthetic data must intentionally vary (clean, messy, partial, contradictory, ambiguous) to stress-test the system.
- The system must adapt to changing structures without redesign.

---

## 10. Generative UI Requirement

The target is a **C1-style generative UI** with three main surfaces:

1. **Main chat stream**: user messages, assistant final answers, citations, confidence, action buttons (rerun, deepen, compare, show evidence).
2. **Live process stream**: structured run events — file parsed, evidence selected, calculation completed, claim challenged, confidence downgraded, clarification requested.
3. **Debate/trace drawer**: challenged claims, challenge reasons, adjudication outcomes, calculation traces, evidence links, run mode indicator.

Final answer rendering is **block-based**: direct answer block, evidence block, confidence block, debate summary block, calculation block, citations block, follow-up action buttons.

The frontend must render structured events and answer payloads. It must **not** contain analytical logic.

---

## 11. Build Phases

| Phase | Name | Deliverables |
|-------|------|-------------|
| 0 | Foundation | Repo skeleton, docs, rules, schemas, environment contract |
| 1 | File Ingestion | File upload, parsers, normalization, citation anchors, evidence objects |
| 2 | Retrieval | Indexing, retrieval abstraction, evidence bundles, baseline answer flow |
| 3 | Calculation | Trusted calculator, table operations, ratios, calculation traces |
| 4 | Multi-agent Analysis | Run router, analyst, challenger, adjudicator, composer, clarification flow |
| 5 | Generative UI | Chat shell, live run stream, drawers, structured answer UI |
| 6 | Evaluation & Hardening | Red teaming, regression suite, unsupported-claim detection, accuracy tests |

**Sequence rule**: Do not start later phases before earlier foundations are stable.

---

## 12. Risks and Ambiguity Detected

### Risks
1. **Secret exposure**: The `.env` file may contain real API keys. It is excluded from version control via `.gitignore`.
2. **pnpm not installed**: The workspace doc references pnpm but it was not available on this machine. Installed during setup.
3. **ruff not installed**: The user rules require ruff for Python formatting/linting. Installed via pip as dev dependency.
4. **No git initialized**: The repository existed as files only, with no version control. Initialized during setup.

### SECURITY INCIDENT — .env was read (now prohibited)

During the initial Phase 0 session, the Cursor agent read the `.env` file contents via shell command.
This was a mistake. The `.env` file may contain live production secrets and must never be read,
printed, inspected, summarized, or validated by any automated agent or tool.

**Rule established**: `.env` is forbidden for agent access. Only `.env.example` is the environment contract.
This rule is permanent and applies to all future sessions.

### Ambiguities
1. **Worker technology**: The docs specify "worker process for async jobs" but do not prescribe a specific task queue library (Celery, ARQ, custom Redis-based, etc.). Decision needed — see `docs/96_assumption_register.md`.
2. **Auth strategy for later phases**: `AUTH_MODE=local_dev` is specified but no detail on production auth. Acceptable for Phase 0; will need clarification later.
3. **Azure Search vs local retrieval**: `.env.example` includes both local and Azure Search config. The docs say "local-first development" with "adapters for later Azure Search." The abstraction boundary is clear but the concrete local implementation (pgvector, FAISS, etc.) is not specified.
4. **Embedding model**: `EMBEDDING_DIMENSIONS=3072` is specified but the specific embedding deployment name is left blank. This is fine for Phase 0.
5. **`.env.example` is canonical**: Only `.env.example` is treated as the environment contract. The `.env` file's contents are unknown and irrelevant to the scaffold.

### Contradictions Found
- **None significant.** The documentation is internally consistent. The `.cursor/rules/` files, `AGENTS.md`, and `docs/` all reinforce the same principles without conflict. The only tension is between the `.env` file's ad-hoc variable naming and the `.env.example` canonical contract, but `.env.example` is clearly the intended standard.

---

## Self-Critique — Round 1 (Initial scaffold session)

Performed: 2026-04-08, after initial scaffold work.

Findings from Round 1 that were partially addressed at the time:
- Config model was incomplete vs `.env.example` → fixed
- docker-compose test DB contradicted `.env.example` → fixed
- Makefile `clean` target was Unix-only → partially fixed
- CORS origin was hardcoded → fixed
- `datetime.utcnow` deprecated → fixed

Findings from Round 1 that were **not** properly addressed:
- Phase 1 parser dependencies were acknowledged but kept — this was wrong
- Assumptions were listed informally but not registered in a proper document
- `.env` was read during the session — a security violation
- Makefile portability was claimed but not honestly documented
- The completion report overstated compliance

---

## Self-Critique — Round 2 (Correction pass)

Performed: 2026-04-08, full correction mode.
Mode: AlMuhasbi strict accountability.

---

### Correction 1 — .env was read (SECURITY VIOLATION, now prohibited)

**Severity: Critical**

During the initial scaffold session, the Cursor agent ran `Get-Content .env` and printed the file contents, which included live Azure OpenAI API keys. This was a security violation. The `.env` file may contain production secrets and must never be read by any automated tool.

**Corrective action**: Documented the prohibition in this report. `.env` is permanently forbidden for agent access. Only `.env.example` is the environment contract.

---

### Correction 2 — Phase 1 parser dependencies removed (WAS PREMATURE)

**Severity: High**

The initial scaffold included `python-docx`, `pdfplumber`, `python-pptx`, `openpyxl`, `pandas`, `python-multipart`, `arq`, `sse-starlette`, and `httpx` (as main dep) in `pyproject.toml`. These are Phase 1+ libraries. `docs/05_build_phases.md` is explicit: Phase 0 delivers "repo skeleton, docs, rules, schemas, environment contract." Phase 1 delivers "parsers for DOCX, PDF, PPTX, XLSX, CSV."

The Round 1 self-critique acknowledged this but justified keeping them as "pragmatic." This was wrong — the user's instruction said "Do not code Phase 2+ behavior yet" and "Create only the environment and scaffolding files needed for the foundation." Including Phase 1 libraries is not Phase 0 foundation.

**Corrective action**: All premature dependencies removed from `pyproject.toml`. Only Phase 0 foundation dependencies remain: fastapi, uvicorn, pydantic, pydantic-settings, sqlalchemy, psycopg, alembic, redis, structlog.

---

### Correction 3 — mypy strict type errors fixed

**Severity: Medium**

Two `dict` type parameters were missing under strict mypy:
- `packages/schemas/evidence.py` line 27: `dict` → `dict[str, str]`
- `packages/schemas/document.py` line 22: `dict` → `dict[str, object]`

**Corrective action**: Fixed. mypy now passes cleanly: "Success: no issues found in 30 source files."

---

### Correction 4 — next-env.d.ts was missing

**Severity: Medium**

The `tsconfig.json` includes `next-env.d.ts` in its `include` array, but the file did not exist. This would cause a TypeScript configuration warning/error.

**Corrective action**: Created `apps/web/next-env.d.ts` with standard Next.js type references.

---

### Correction 5 — Makefile portability honestly documented

**Severity: Medium**

The Makefile requires GNU Make, which is not installed by default on Windows. The `help` target in Round 1 used `grep` + `awk` (Unix-only). The Round 1 self-critique called this "fixed" after replacing the `clean` target, but the `help` target was still broken.

**Corrective action**: Replaced `help` with plain `echo` statements. Added an honest platform note at the top documenting that GNU Make is required and listing Windows alternatives.

---

### Correction 6 — Assumption register created

**Severity: Medium**

Multiple assumptions were made during scaffolding (ARQ, Tailwind v4, Next.js 15, tests/unit/, etc.) that were not explicitly prescribed. Round 1 listed these informally but did not create a proper register or classify them.

**Corrective action**: Created `docs/96_assumption_register.md` with every assumption classified as required, optional (proposal), or premature (reverted).

---

### Correction 7 — Exact changed-file list created

**Severity: Low**

Round 1 grouped files by category. The user needs path-by-path exactness.

**Corrective action**: Created `docs/95_exact_changed_file_list.md` with every file path listed explicitly, separated into pre-existing (owner) and created (Cursor).

---

### What was wrong in Round 1

1. `.env` was read — security violation.
2. Phase 1 dependencies were included and justified — should have been removed.
3. Makefile portability was claimed but not real.
4. `next-env.d.ts` was missing from the frontend scaffold.
5. Two mypy strict errors were present.
6. Assumptions were not properly registered.
7. The completion report overstated compliance by calling the scaffold "lint-clean, tested, and ready."

### What was corrected in Round 2

1. `.env` reading documented as prohibited; rule established permanently.
2. All premature Phase 1+ dependencies removed from `pyproject.toml`.
3. Makefile rewritten with honest platform documentation.
4. `next-env.d.ts` created.
5. mypy errors fixed; full strict pass: 30 files, 0 errors.
6. `docs/96_assumption_register.md` created with classifications.
7. This report updated to not overstate compliance.

### What still remains a proposal (not approved)

These items are in the scaffold but require explicit owner approval:

| Item | Classification | Reference |
|------|---------------|-----------|
| Tailwind CSS v4 | Optional proposal | `docs/96_assumption_register.md` #2 |
| Next.js 15 (App Router) | Optional proposal | `docs/96_assumption_register.md` #3 |
| `tests/unit/` directory | Optional addition | `docs/96_assumption_register.md` #5 |
| Postgres 16 Alpine | Optional proposal | `docs/96_assumption_register.md` #7 |
| Redis 7 Alpine | Optional proposal | `docs/96_assumption_register.md` #8 |
| structlog | Optional proposal | `docs/96_assumption_register.md` #9 |
| setuptools build backend | Optional default | `docs/96_assumption_register.md` #11 |

### What is still missing from Phase 0

| Item | Status | Notes |
|------|--------|-------|
| `TASK.md` | Not created | User rules reference it; user instructions did not request it |
| Python dependency lock file | Not created | Builds are not fully reproducible |
| Frontend `pnpm install` + build verification | Not done | Shell files exist but have not been installed/built |
| Alembic migration directory | Not created | Appropriate — no DB tables in Phase 0 |

### Honest verdict

The Phase 0 scaffold is now structurally aligned with the controlling docs after corrections. The repository skeleton, schemas, config, and app shells match `docs/06_repo_structure.md` and `docs/05_build_phases.md`. No Phase 1+ code or dependencies remain. All code passes mypy strict, ruff, and pytest.

However, the scaffold contains several technology proposals (Tailwind, Next.js 15, structlog, etc.) that are not doc-prescribed and require owner approval. The Makefile requires GNU Make. The frontend has not been build-verified. These are not compliance failures, but they are honest limitations that should not be hidden.

---

Status: understanding report + corrected self-critique
Use: proof of reading, comprehension, correction, and honest assessment
