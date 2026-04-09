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

## Schema interpretation

`FieldDefinition` distinguishes:
- `source_field_name` — the actual column name in raw data (e.g., `EID`)
- `semantic_name` — the normalized meaning (e.g., `establishment_eid`)

This separation is required because raw field names like `EID` may appear
with overloaded meanings across different tables.

`IdentifierRule` is a typed model (not `list[str]`) with `pattern`, `scope`, and `description`.

`JoinRule.join_type` uses the `JoinType` enum (not a free string).

### Semantic authority hierarchy

1. **Global governance/safety rules** from `docs/20_data_dictionary_and_identifier_rules.md` — hard-coded system-wide constraints (e.g., "EID is per-table scoped")
2. **User-supplied per-table data dictionary** (e.g., `data_type.xlsx`) — explicit field definitions, join rules, and identifier scoping for specific tables. When more specific than global rules, the user's per-table mapping takes precedence for that table.
3. **Parsed file metadata** — `detected_schema`, `sheet_names`, column headers — supporting fallback source only. Must not override a data dictionary when one exists.

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
