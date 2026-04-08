# GenUIWar — Run and Event Schema

## Goal
Define the streaming contract that powers:
- live telemetry
- visible agent work
- reuse vs rerun honesty
- debate visibility
- auditability

## Run
A run is a discrete analytical execution triggered by:
- file upload preparation
- background analysis
- a user question
- a targeted follow-up
- a deep rerun
- a clarification path

### Run categories
- document_preparation
- background_analysis
- question_answering
- targeted_followup
- deep_rerun
- clarification_required

### Run modes
- reuse
- hybrid
- fresh

## Core run fields
- run_id
- conversation_id
- trigger_message_id
- parent_run_id
- run_category
- run_mode
- status
- scope
- question
- decision_reason
- created_at
- started_at
- completed_at

## Run statuses
- queued
- running
- waiting_for_clarification
- completed
- failed
- cancelled

## Event
An event is a structured, streamable record of something meaningful that happened during a run.

Events are not unrestricted hidden reasoning. They are useful observable telemetry.

## Core event fields
- event_id
- run_id
- event_index
- event_type
- event_group
- agent_name
- status
- title
- summary
- payload
- created_at
- is_user_visible

## Recommended event groups
- run_lifecycle
- ingestion
- linking
- retrieval
- analysis
- calculation
- challenge
- adjudication
- clarification
- answer_rendering

## Examples of visible events
- run.mode_selected
- ingestion.parse_completed
- retrieval.bundle_selected
- calculation.completed
- challenge.missing_evidence_flagged
- adjudication.claim_rejected
- clarification.requested
- answer.completed

## Rule
Every final answer must link back to the run, evidence bundle, calculation results, claim ledger, and adjudication outcome that produced it.

---
Status: foundational run/event contract
Use: backend streaming contract and frontend rendering guide
