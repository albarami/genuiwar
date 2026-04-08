# GenUIWar — Evidence Rules

## Core rule
**No free facts.**

No important final statement may appear unless it is supported by:
- source evidence,
- verified calculation,
- or both.

## Evidence rules
1. Every important claim must map to a claim ledger entry.
2. Every claim must be typed as:
   - direct
   - derived
   - model_based
3. Every supported claim must cite one or more evidence anchors.
4. Every numeric claim beyond a direct raw value must include a calculation trace.
5. Unsupported claims must be rejected or rewritten with explicit uncertainty.
6. If evidence is insufficient, the system must either:
   - downgrade confidence,
   - ask a clarification question,
   - or decline to conclude.

## Claim rules
### Direct
Directly grounded in source material.

### Derived
Computed from source material using deterministic logic.

### Model-based
Interpretive, inferential, or scenario-dependent.

These categories must never be merged invisibly.

## Confidence rules
Use explicit confidence grades:
- high
- moderate
- emerging
- low
- unresolved

## Clarification rules
The system must ask the user a clarification question when:
- schema meaning is unclear
- denominator is unclear
- file structure is ambiguous
- question intent is underspecified
- evidence is insufficient for a reliable answer

## Review rules
The challenger must attack high-impact claims in AlMuhasbi or Devil’s Advocate mode.
The adjudicator is the final gate before answer release.

## Final answer rules
A final answer must:
- be backed by approved claims only
- expose confidence honestly
- never hide missing support behind fluent wording

---
Status: foundational evidence policy
Use: core trust rules for prompting, validation, and adjudication
