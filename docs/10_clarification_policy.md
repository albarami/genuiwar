# GenUIWar — Clarification Policy

## Goal
Define when the system must ask the user for clarification instead of guessing.

## Core principle
Accuracy is non-negotiable.
If the system cannot safely determine meaning, scope, or assumptions, it must ask a clarification question.

## Clarification triggers
The system should ask clarification questions when:
- a file structure is ambiguous
- a schema mapping is unclear
- a denominator is missing or ambiguous
- multiple possible interpretations exist
- the user question is underspecified
- the requested comparison lacks a clear time window
- prior outputs do not cleanly answer the current question
- evidence is insufficient for a reliable conclusion

## Examples
### File ambiguity
“I found two columns that may both represent workforce exits. Which one should be treated as the primary exit indicator?”

### Question ambiguity
“Do you want the answer based on all uploaded files or only the latest file?”

### Denominator ambiguity
“Should the percentage be calculated against total firms, active firms, or firms in the selected sector only?”

## Rules
1. Clarification must happen before deep execution continues.
2. The system must record the uncertainty that triggered the clarification.
3. Clarification should be short, specific, and decision-oriented.
4. The system must not ask unnecessary clarification questions when evidence is already sufficient.

## Output handling
If the user does not answer, the system should:
- pause the deep run, or
- answer only the safe supported portion while clearly marking the unresolved part

---
Status: clarification policy
Use: rulebook for safe question-asking behavior
