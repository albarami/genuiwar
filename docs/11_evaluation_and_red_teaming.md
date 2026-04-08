# GenUIWar — Evaluation and Red Teaming

## Goal
Define how the system will be tested, challenged, and hardened.

## Core principle
A convincing answer is not enough.
The system must be evaluated for:
- evidence support
- calculation accuracy
- retrieval quality
- challenge depth
- adjudication correctness
- clarification behavior
- UI trace honesty

## Evaluation categories
### 1. Evidence support
Check whether important claims map to valid evidence anchors.

### 2. Calculation accuracy
Check whether numeric claims match trusted calculator outputs.

### 3. Retrieval quality
Check whether the selected evidence bundle is relevant and sufficient.

### 4. Claim challenge quality
Check whether the challenger catches:
- unsupported claims
- missing denominators
- false precision
- contradictions
- shallow synthesis

### 5. Adjudication quality
Check whether the adjudicator:
- rejects unsupported claims
- downgrades overstated claims
- requests clarification when needed

### 6. Clarification behavior
Check whether the system asks questions at the right time instead of guessing.

## Red-team modes
### AlMuhasbi mode
Strict accountability review focused on hidden assumptions, weakness, and overclaiming.

### Devil’s Advocate mode
Adversarial challenge focused on breaking the draft answer and exposing fragile logic.

## Minimum evaluation artifacts
- golden question sets
- contradictory file sets
- ambiguous schema sets
- denominator trap cases
- unsupported-claim detection tests
- regression tests for previously fixed failures

---
Status: evaluation and hardening policy
Use: source of truth for quality assurance and adversarial review
