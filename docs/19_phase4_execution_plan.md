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

## Deliverables

1. `packages/schemas/dataset_context.py` — DatasetContext, TableContext, FieldDefinition, JoinRule, SourceLocator
2. `packages/agents/llm_adapter.py` — LLMAdapter ABC + Azure + Deterministic
3. `packages/schemas/answer.py` — FinalAnswerPayload, AnswerBlock, AnswerBlockType
4. `packages/agents/` — 6 agent contracts with dual implementations
5. `packages/storage/` — Phase 4 repository ABCs + in-memory implementations
6. `packages/orchestration/events.py` — EventEmitter
7. `packages/orchestration/engine.py` — RunOrchestrator
8. `packages/governance/` — no_free_facts + identifier_safety validators
9. `apps/api/routes/runs.py` — runs API
10. Tests for all of the above

## Event types

Event names are aligned with `docs/07_run_event_schema.md` and extended
for Phase 4 where needed.

Aligned with existing contract: run.mode_selected, retrieval.bundle_selected,
calculation.completed, challenge.missing_evidence_flagged,
adjudication.claim_rejected, clarification.requested, answer.completed

Phase 4 extensions: run.started, run.completed, analysis.draft_completed,
analysis.claim_ledger_created, challenge.review_completed,
challenge.claim_flagged, adjudication.completed

## Governance

- Pre-compose: validate claims safe for composition + identifier usage
- Post-compose: validate answer has no free facts
- Identifier safety: no unscoped identifiers, no undeclared joins, no qualitative-as-quantitative

---

Status: Phase 4 execution plan
Use: bounded implementation guide for Phase 4 only
