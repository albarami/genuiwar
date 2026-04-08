# GenUIWar — Build Phases

## Purpose
Define the implementation sequence so the project does not jump into a fragile prototype.

## Phase 0 — Foundation
Deliver:
- repo skeleton
- docs backbone
- Cursor rules
- AGENTS.md
- README.md
- environment contract
- schemas for runs, events, evidence, claims, calculations

## Phase 1 — File ingestion
Deliver:
- file upload
- parsers for DOCX, PDF, PPTX, XLSX, CSV
- normalization
- citation anchors
- evidence objects

## Phase 2 — Retrieval
Deliver:
- indexing
- retrieval abstraction
- evidence bundles
- baseline answer flow with citations

## Phase 3 — Calculation
Deliver:
- trusted calculator service
- table operations
- ratios and comparisons
- calculation trace objects

## Phase 4 — Multi-agent analysis
Deliver:
- run router
- primary analyst
- challenger
- adjudicator
- composer
- clarification flow

## Phase 5 — Generative UI
Deliver:
- chat shell
- live run stream
- evidence drawer
- debate drawer
- final structured answer UI

## Phase 6 — Evaluation and hardening
Deliver:
- red teaming
- regression suite
- unsupported-claim detection
- retrieval evaluation
- calculation accuracy tests

## Sequence rule
Do not start later phases before earlier foundations are stable.

---
Status: phased build plan
Use: implementation order and project control
