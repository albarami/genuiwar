# GenUIWar — Data Dictionary and Identifier Rules

Generated: 2026-04-09

---

## Purpose

Define how the system interprets structured ministry datasets, identifier fields,
join logic, and qualitative vs quantitative evidence. Agents must not guess
identifier meanings or table semantics.

## Identifier rules

### Establishment identifier (EID)

- Field pattern: `establishment_eid`, `eid`, `EID`, `est_id`
- Scope: **per-table** — an EID in one table does not automatically mean the same
  entity as an EID in another table
- Rule: do NOT assume global scope without an explicit `JoinRule` declaration

### Person identifier (QID)

- Field pattern: `person_qid`, `qid`, `QID`, `person_id`
- Scope: **per-table** — same scoping rule as EID

### General identifier rule

- Any field with `field_type=IDENTIFIER` is scoped to its containing table
- Cross-table use requires a declared `JoinRule` in `DatasetContext.join_rules`
- Ambiguous identifier fields MUST trigger a clarification question

## Per-table semantic mapping

Before any analytical operation:
1. Every table must have a `TableContext` with field definitions
2. Every identifier field must have `identifier_scope` set
3. Cross-table joins must be declared as `JoinRule` entries
4. If mapping is incomplete, the system must ask for clarification

## Qualitative vs quantitative evidence

- **Quantitative**: structured tables with numeric data, identifiers, dates
  - `evidence_type = EvidenceSourceType.QUANTITATIVE`
  - Primary backbone for analytical claims
- **Qualitative**: interview Q&A, narrative documents, free-text reports
  - `evidence_type = EvidenceSourceType.QUALITATIVE`
  - Secondary layer that may enrich interpretation
  - Must NOT silently override structured numeric findings

## Semantic authority hierarchy

1. **This document** — hard-coded governance rules
2. **User-supplied data dictionary** (e.g., `data_type.xlsx`) — explicit field definitions
3. **Parsed file metadata** — column headers, detected schemas — supporting source only

The system must not infer identifier meaning from parsed metadata alone
when a data dictionary source exists.

## What must be clarified before analytical use

- Identifier meaning when not in the data dictionary
- Join logic when tables share field names but no `JoinRule` exists
- Source-field overloading (e.g., "EID" meaning different things in two tables)
- Whether a qualitative source should influence a quantitative finding
- Denominator scope when multiple interpretations exist

## Governance checks

The `validate_identifier_usage` function checks:
- No claim uses an identifier without per-table mapping
- No cross-table join without a declared `JoinRule`
- No source-field overloading without explicit scoping
- No qualitative evidence silently treated as quantitative

---

Status: data dictionary and identifier rules
Use: governance reference for schema interpretation and identifier safety
