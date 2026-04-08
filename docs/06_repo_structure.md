# GenUIWar — Repository Structure

## Purpose
Define the repo layout so parsing, retrieval, orchestration, calculations, UI, and governance remain separate and testable.

## Target structure
```text
genuiwar/
  .cursor/
    rules/
  docs/
  apps/
    api/
    web/
    worker/
  packages/
    schemas/
    orchestration/
    agents/
    parsers/
    retrieval/
    calculators/
    governance/
    storage/
    prompts/
    evaluation/
    synthetic_data/
    shared/
  infra/
  tests/
  AGENTS.md
  README.md
  .env
  .env.example
```

## apps
### apps/api
Backend API, routes, streaming, dependencies, request orchestration.

### apps/web
Frontend generative UI.

### apps/worker
Background jobs for parsing, indexing, and deeper runs.

## packages
### schemas
Typed contracts shared across the system.

### orchestration
Run engine and workflow state machine.

### agents
Concrete agent definitions and prompts.

### parsers
File-type specific parsing and normalization.

### retrieval
Evidence search and bundle creation.

### calculators
Trusted numeric logic.

### governance
No-free-facts enforcement, provenance, confidence, adjudication policy.

### storage
Storage adapters and persistence helpers.

### prompts
Versioned prompts and templates.

### evaluation
Red teaming, golden sets, regressions.

### synthetic_data
Synthetic files, tables, and messy scenarios.

### shared
Small cross-cutting helpers only.

## Rule
Business logic must not collapse into giant utility files or API routes.

---
Status: repository layout guide
Use: source-of-truth repo organization for Cursor
