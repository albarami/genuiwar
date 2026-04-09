# GenUIWar — Phase 4 Execution Plan (Multi-Agent Orchestration)

Generated: 2026-04-09
Branch: `feat/phase4-orchestration`

---

## Scope

Phase 4 delivers multi-agent analysis per `docs/05_build_phases.md`:
- Run router, primary analyst, challenger, adjudicator, composer, clarification flow
- Claim ledger enforcement, run/event emission, governance validation
- Schema interpretation / data dictionary awareness
- Dual-mode agents: deterministic (tests/dev) + Azure OpenAI (runtime)

## What is implemented

### Governance wired into orchestrator

- `validate_claims_safe_for_composition` — called after adjudication, before composition
- `validate_identifier_usage` — called before composition
- `validate_answer_no_free_facts` — called after composition, before release
- Violations emit typed events and halt the run with `FAILED` status

### Agent factory

- `packages/agents/factory.py` reads `AGENT_MODE` config
- `deterministic` (default): rule-based agents for tests/dev
- `azure`: Azure OpenAI-backed agents for runtime
- Runs API uses the factory, not hardcoded agents

### Retriever injection

- `RunOrchestrator` accepts a `BaseRetriever` via constructor
- No hardcoded `LocalKeywordRetriever` inside the orchestrator
- Current default: `LocalKeywordRetriever` injected by the runs route

### DatasetContext loader (real operational path)

- `packages/agents/context_loader.py` provides `build_dataset_context()`
- The runs API calls it at runtime, building context from:
  - registered file metadata (from prior uploads)
  - optional user-supplied `DatasetContext` (authoritative where it covers tables)
  - default identifier rules (always included)
- User-supplied per-table fields are never overridden by parsed metadata
- Parsed metadata fills only gaps (fields the user dict does not define)
- File upload route registers `FileDocument` objects for the context loader to use

### Schema interpretation

- `FieldDefinition.source_field_name` = raw column name
- `FieldDefinition.semantic_name` = normalized meaning
- `IdentifierRule` = typed model with pattern, scope, description
- `JoinRule.join_type` = `JoinType` enum

### Semantic authority

1. Global governance rules — always applied
2. User-supplied data dictionary — authoritative for tables it covers
3. Parsed file metadata — fills gaps only, never overrides user mapping

## What is deferred

- `data_type.xlsx` file parser (loader accepts DatasetContext directly; no raw Excel parser yet)
- Azure adapter live testing
- Postgres persistence for Phase 4 artifacts
- Package README updates

---

Status: Phase 4 execution plan (implemented)
Use: bounded implementation guide for Phase 4
