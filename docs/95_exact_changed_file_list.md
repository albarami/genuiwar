# GenUIWar — Exact Changed-File List (Phase 0 Foundation)

Generated: 2026-04-08 (Correction pass)
Source: `git status --short --untracked-files=all`

---

## Pre-existing files (authored by the owner, NOT created by Cursor)

These files existed in the repository before Cursor work began.
They are untracked in git because git was not initialized until the scaffold session.

```
.cursor/rules/00_architecture.mdc
.cursor/rules/01_agent_behavior.mdc
.cursor/rules/02_evidence_discipline.mdc
.cursor/rules/03_coding_standards.mdc
.env.example
AGENTS.md
README.md
docs/00_project_mission.md
docs/00_project_setup_checklist.md
docs/01_system_architecture.md
docs/02_agent_workflow.md
docs/03_evidence_rules.md
docs/04_ui_ux_contract.md
docs/05_build_phases.md
docs/06_repo_structure.md
docs/07_run_event_schema.md
docs/08_claim_ledger_schema.md
docs/09_synthetic_data_strategy.md
docs/10_clarification_policy.md
docs/11_evaluation_and_red_teaming.md
docs/12_api_contract_overview.md
docs/13_first_cursor_build_brief.md
```

## Files created by Cursor (Phase 0 scaffold)

### Root configuration files

```
.gitignore
.python-version
pyproject.toml
package.json
pnpm-workspace.yaml
docker-compose.yml
Makefile
```

### Documentation created by Cursor

```
docs/95_exact_changed_file_list.md
docs/96_assumption_register.md
docs/97_git_strategy.md
docs/98_initial_execution_plan.md
docs/99_cursor_understanding_report.md
```

### apps/api (FastAPI backend shell)

```
apps/__init__.py
apps/api/__init__.py
apps/api/dependencies.py
apps/api/main.py
apps/api/README.md
apps/api/routes/__init__.py
apps/api/routes/health.py
```

### apps/web (Next.js frontend shell)

```
apps/web/next.config.ts
apps/web/next-env.d.ts
apps/web/package.json
apps/web/postcss.config.mjs
apps/web/README.md
apps/web/src/app/globals.css
apps/web/src/app/layout.tsx
apps/web/src/app/page.tsx
apps/web/tsconfig.json
```

### apps/worker (worker shell)

```
apps/worker/__init__.py
apps/worker/main.py
apps/worker/README.md
```

### packages/schemas (typed domain contracts)

```
packages/__init__.py
packages/schemas/__init__.py
packages/schemas/calculation.py
packages/schemas/claim.py
packages/schemas/clarification.py
packages/schemas/conversation.py
packages/schemas/document.py
packages/schemas/enums.py
packages/schemas/evidence.py
packages/schemas/README.md
packages/schemas/run.py
```

### packages/shared (config + helpers)

```
packages/shared/__init__.py
packages/shared/config.py
packages/shared/README.md
```

### packages (placeholder skeletons)

```
packages/agents/__init__.py
packages/agents/README.md
packages/calculators/__init__.py
packages/calculators/README.md
packages/evaluation/__init__.py
packages/evaluation/README.md
packages/governance/__init__.py
packages/governance/README.md
packages/orchestration/__init__.py
packages/orchestration/README.md
packages/parsers/__init__.py
packages/parsers/README.md
packages/prompts/__init__.py
packages/prompts/README.md
packages/retrieval/__init__.py
packages/retrieval/README.md
packages/storage/__init__.py
packages/storage/README.md
packages/synthetic_data/__init__.py
packages/synthetic_data/README.md
```

### infra

```
infra/deployment/README.md
infra/docker/init-test-db.sql
infra/docker/README.md
infra/scripts/README.md
```

### tests

```
tests/__init__.py
tests/conftest.py
tests/e2e/__init__.py
tests/e2e/README.md
tests/integration/__init__.py
tests/integration/README.md
tests/unit/__init__.py
tests/unit/test_schemas.py
```

---

## Total counts

- Pre-existing (owner-authored): 22 files
- Created by Cursor: 71 files
- Total untracked: 93 files

---

Status: exact changed-file list
Use: auditability record for Phase 0 scaffold
