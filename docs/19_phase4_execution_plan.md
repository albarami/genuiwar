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

## Out of scope

- Generative UI (Phase 5)
- Evaluation / red teaming (Phase 6)
- Full autonomous multi-agent behavior beyond defined roles

## Architecture

Calculator is the existing Phase 3 service, not a new agent.
Agents are dual-mode: deterministic for tests, Azure OpenAI for runtime.
Agent mode is set by explicit `AGENT_MODE` config, not inferred.
Retriever is injected into the orchestrator, not hardcoded.

## What is implemented

- **Governance validators wired into orchestrator pipeline:**
  - `validate_claims_safe_for_composition` called after adjudication
  - `validate_identifier_usage` called before composition
  - `validate_answer_no_free_facts` called after composition
  - Violations emit events and halt the run with `FAILED` status
- **Agent factory** (`packages/agents/factory.py`) driven by `AGENT_MODE` config
- **Retriever injected** into RunOrchestrator — no hardcoded `LocalKeywordRetriever`
- **DatasetContext loader** (`packages/agents/context_loader.py`):
  - Builds context from parsed file metadata as fallback
  - Accepts user-supplied DatasetContext that takes precedence
  - Always includes default identifier rules (EID, QID)
- All 6 dual-mode agent contracts
- Phase 4 storage repositories (in-memory)
- Run/event emission with typed events

## Schema interpretation

`FieldDefinition` distinguishes:
- `source_field_name` — actual column name in raw data
- `semantic_name` — normalized meaning (e.g., `establishment_eid`)

`IdentifierRule` is a typed model with `pattern`, `scope`, `description`.
`JoinRule.join_type` uses the `JoinType` enum.

### Semantic authority hierarchy

1. **Global governance/safety rules** from `docs/20` — system-wide constraints
2. **User-supplied per-table data dictionary** — takes precedence for specific tables
3. **Parsed file metadata** — supporting fallback only

## Event types

Event names are aligned with `docs/07_run_event_schema.md` and extended
for Phase 4 where needed, including governance violation events.

## What is deferred

- Azure adapter live testing (requires running Azure endpoint)
- `data_type.xlsx` file parser (context_loader accepts DatasetContext directly)
- Postgres persistence for Phase 4 artifacts
- Package README updates

---

Status: Phase 4 execution plan (implemented)
Use: bounded implementation guide for Phase 4
