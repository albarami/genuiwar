# packages/schemas

Typed Pydantic v2 contracts shared across the entire system.

All first-class domain objects live here: Conversation, Message, FileDocument,
EvidenceChunk, Run, RunEvent, ClaimLedgerEntry, CalculationResult, ClarificationRequest.

Enums for states, types, and grades are in `enums.py`.

No business logic belongs here — only data shape definitions.
