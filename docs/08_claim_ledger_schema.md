# GenUIWar — Claim Ledger Schema

## Goal
Define the structure that enforces no-free-facts behavior.

## Core rule
Every important final answer statement must map to one or more claim ledger entries.

## Claim typing
Every claim must be tagged as:
- direct
- derived
- model_based

## Core claim fields
- claim_id
- run_id
- parent_claim_id
- claim_text
- claim_type
- claim_scope
- support_status
- confidence_grade
- materiality
- evidence_refs
- calculation_result_ids
- assumptions
- challenge_flags
- adjudication_status
- adjudication_reason
- created_by_agent
- created_at

## Support status
- supported
- partially_supported
- unsupported
- needs_clarification

## Confidence grades
- high
- moderate
- emerging
- low
- unresolved

## Materiality
- high
- medium
- low

High-materiality claims must always be challenged.

## Challenge flags
Recommended flags:
- missing_evidence
- missing_calculation_trace
- denominator_unclear
- scope_overreach
- false_precision
- contradictory_evidence
- weak_interpretation
- schema_mapping_unclear
- time_window_unclear
- claim_too_broad
- needs_user_clarification

## Adjudication status
- approved
- downgraded
- rejected
- pending

Rejected claims must never enter final output.

## Lifecycle
1. claim created
2. evidence attached
3. calculations attached if needed
4. challenger reviews
5. flags added
6. adjudicator decides
7. composer uses only approved / properly downgraded claims

---
Status: claim integrity contract
Use: source of truth for support tracking, challenge, and adjudication
