# GenUIWar — UI / UX Contract

## Goal
Define the product behavior and rendering contract for a C1-style generative UI with visible analytical execution.

## Experience target
The user should experience:
- a conversational interface
- live streamed process telemetry
- visible agent activity
- visible debate and adjudication
- a final structured generative UI answer

## Main visible surfaces
### 1. Main chat stream
Shows:
- user messages
- assistant final answer
- citations
- confidence
- actions such as rerun, deepen, compare, show evidence

### 2. Live process stream
Shows structured run events such as:
- file parsed
- evidence selected
- calculation completed
- claim challenged
- confidence downgraded
- clarification requested

This stream must show useful telemetry, not unrestricted chain-of-thought.

### 3. Debate / trace drawer
Shows:
- challenged claims
- reasons for challenge
- adjudication outcomes
- calculation traces
- evidence links
- whether the answer came from reuse, hybrid, or fresh run

## Final answer rendering
The final answer should be structured into blocks such as:
- direct answer block
- evidence block
- confidence block
- debate summary block
- calculation block
- citations block
- follow-up action buttons

## Reuse vs rerun transparency
The UI must show whether the answer came from:
- prior validated outputs
- a hybrid run
- a fresh run

## Clarification behavior
If the system needs clarification, the UI must present the question clearly and suspend deep execution rather than continue guessing.

---
Status: foundational UX contract
Use: source of truth for frontend behavior and answer rendering
