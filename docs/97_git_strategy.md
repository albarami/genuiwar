# GenUIWar — Git Branch Strategy

Generated: 2026-04-08

---

## Branching Model

Use a simplified trunk-based development model suitable for a small team building in phases.

### Primary Branches

| Branch | Purpose | Protection |
|--------|---------|-----------|
| `main` | Stable, reviewed code only. Every commit on main should be buildable. | Protected: require PR review |
| `develop` | Integration branch for current phase work. Merges to main at phase milestones. | Protected: require PR |

### Working Branches

Use short-lived feature branches off `develop`:

```
feat/phase0-foundation
feat/phase0-schemas
feat/phase1-file-upload
feat/phase1-parsers-docx
feat/phase1-parsers-xlsx
fix/parser-encoding-issue
test/schema-validation
docs/update-api-contract
```

### Naming Convention

Follow conventional commit scopes:
- `feat/<scope>-<description>` — new feature work
- `fix/<scope>-<description>` — bug fixes
- `test/<scope>-<description>` — test additions
- `refactor/<scope>-<description>` — structural improvements
- `docs/<description>` — documentation changes
- `chore/<description>` — tooling, config, dependencies

### Commit Message Format

```
<type>(<scope>): <short description>

<optional body explaining why>
```

Examples:
```
feat(schemas): add Run and RunEvent Pydantic models
feat(parsers): implement DOCX parser with citation anchors
fix(parsers): handle empty table cells in XLSX parser
test(schemas): add claim ledger entry validation tests
docs: update execution plan after Phase 0 completion
```

---

## Phase-Based Workflow

### Phase 0 — Foundation
1. Create `feat/phase0-foundation` from `main`
2. All Phase 0 work goes into this branch
3. When Phase 0 is stable and reviewed → PR to `develop` → PR to `main`

### Phase 1 — File Ingestion
1. Create `feat/phase1-*` branches from `develop`
2. Merge completed features into `develop`
3. When Phase 1 is stable → PR to `main`

### Later Phases
Same pattern. Each phase has its own feature branches merging into `develop`, then `develop` merges to `main` at milestones.

---

## Rules

1. Never push directly to `main`.
2. Never force-push to `main` or `develop`.
3. Every PR must pass lint, typecheck, and tests before merge.
4. Atomic commits — one logical change per commit.
5. No debug prints, TODO hacks, or commented-out code in commits.
6. `.env` must never be committed. Only `.env.example` is tracked.
7. Run `ruff check`, `ruff format --check`, and `pytest` before committing Python changes.

---

## Initial State

- Repository initialized locally: 2026-04-08
- Remote: `https://github.com/albarami/genuiwar`
- No pushes yet — awaiting owner review of initial scaffold
- First commit will be the Phase 0 foundation scaffold

---

Status: git strategy document
Use: branch and commit workflow reference
