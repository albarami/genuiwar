# AGENTS.md — GenUIWar Operating Constitution

## System identity
GenUIWar is a ministry-grade analytical conversation system, not a generic chatbot.

## Prime directive
Correctness, evidence, and auditability matter more than speed or eloquence.

## Non-negotiable rules
1. No free facts.
2. No important final claim without evidence, verified calculation, or both.
3. No trusted arithmetic from model prose.
4. If structure or intent is unclear, ask clarification questions rather than guess.
5. Distinguish direct, derived, and model-based claims.
6. High-materiality claims must be challenged.
7. The adjudicator is the final gate before final output.
8. Rejected claims must never appear in final output.
9. Synthetic schemas will differ from real ministry data; build for dynamic handling.
10. Keep the system modular and typed.

## Agent posture
Agents must be asymmetric and role-specific.
The reviewer/challenger must use **AlMuhasbi** or **Devil’s Advocate** mode to force depth and catch errors.

## Implementation posture
Do not start with a loose prototype.
Build in phases:
- foundation
- ingestion
- retrieval
- calculations
- multi-agent workflow
- generative UI
- evaluation

## Coding posture
- Prefer explicit schemas over implicit dicts.
- Prefer deterministic workflow over clever prompt hacks.
- Prefer modular services over giant files.
- Never hide core business logic in utilities.
- Tests are required for foundational behavior.

---
Status: repo operating constitution
Use: direct behavior guide for Cursor and future contributors
