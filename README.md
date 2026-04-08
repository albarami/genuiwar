# GenUIWar

GenUIWar is a ministry-grade analytical conversation system for uploaded files with:
- structured multi-agent analysis
- live visible execution
- evidence-backed answers
- tool-verified calculations
- explicit confidence
- a generative UI experience

## What it is
A controlled analytical platform with:
- file ingestion
- retrieval
- calculations
- challenge and adjudication
- structured answer rendering

## What it is not
- a generic chatbot
- a free-form hidden reasoning tool
- a prose calculator
- a recommendation engine by default

## Core rules
- No free facts.
- Numeric claims must be traceable.
- Unsupported claims must not survive.
- Clarification is required when ambiguity blocks safe interpretation.
- Synthetic schemas must be handled dynamically.

## Main docs
Read these first:
- `docs/00_project_mission.md`
- `docs/01_system_architecture.md`
- `docs/02_agent_workflow.md`
- `docs/03_evidence_rules.md`
- `docs/04_ui_ux_contract.md`
- `docs/05_build_phases.md`
- `docs/06_repo_structure.md`
- `docs/07_run_event_schema.md`
- `docs/08_claim_ledger_schema.md`
- `docs/09_synthetic_data_strategy.md`
- `docs/10_clarification_policy.md`
- `docs/11_evaluation_and_red_teaming.md`
- `docs/12_api_contract_overview.md`
- `docs/13_first_cursor_build_brief.md`

## Cursor control files
- `.cursor/rules/00_architecture.mdc`
- `.cursor/rules/01_agent_behavior.mdc`
- `.cursor/rules/02_evidence_discipline.mdc`
- `.cursor/rules/03_coding_standards.mdc`

## Development posture
Build locally first with synthetic data.
Connect real ministry data later through adapters, not a redesign.

## Next step
Use `docs/13_first_cursor_build_brief.md` as the first exact implementation task for Cursor.

---
Status: repo entry file
Use: first-read project overview
