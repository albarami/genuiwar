# Phase 5 — Generative UI Implementation Plan (Final Revision)

## Pre-work
- Pull merged main (PR #4)
- Create branch feat/phase5-generative-ui from main
- Add Tailwind CSS v4 back to apps/web/package.json
- Run pnpm install in apps/web
- Create docs/21_phase5_execution_plan.md before coding

## 1. Product goal
Phase 5 delivers a professional, typed, block-based generative UI shell for GenUIWar.
The UI must feel structured, inspectable, and trustworthy.
It must render backend outputs cleanly without embedding analytical logic in the frontend.

This phase does NOT deliver:
- true live event streaming
- clarification resume
- conversation persistence
- frontend-driven reasoning
- new orchestration behavior

## 2. Backend reality for Phase 5
Phase 5 execution model is:

- synchronous backend
- post-run rendering
- no SSE
- no polling
- no progressive event arrival during execution

Current run flow:
- POST /api/v1/runs blocks until the run completes
- the frontend shows a loading state while waiting
- once RunResult arrives, the frontend renders:
  - run status
  - post-run event timeline
  - structured answer blocks
  - drawers and inspection surfaces

Do not describe this as live streaming.
The correct wording is:
- typed block-based post-run generative rendering

## 3. Required backend delta for Phase 5
Phase 5 requires one small backend addition for exact evidence resolution:

- add get_by_id(chunk_id: UUID) -> EvidenceChunk | None to ChunkRepository
- implement get_by_id in the in-memory chunk repository
- add GET /api/v1/evidence/chunk/{chunk_id} to apps/api/routes/evidence.py

Reason:
- claim.evidence_refs are treated as EvidenceChunk.chunk_id references in Phase 5
- EvidenceDrawer must resolve exact referenced chunks, not file-scoped chunk lists

## 4. Generative UI contract
The frontend is a typed, block-based, post-run generative interface.

The answer is never rendered as one large text blob.
Each AnswerBlock is rendered independently through a typed block registry.

Required block types:
- direct_answer
- evidence
- confidence
- debate_summary
- calculation
- citations

The block registry maps:
AnswerBlockType -> React component

This must be extensible without switch-statement sprawl.

## 5. UI states
Supported frontend states:

- Empty
  - no run submitted yet
  - render prompt composer only

- Loading
  - POST /runs is in flight
  - render loading shell / spinner / "Running analysis..."

- Answer
  - run completed
  - render:
    - post-run event timeline
    - structured answer blocks
    - evidence / debate / calc drawers

- Clarification
  - run returned waiting_for_clarification
  - render ClarificationCard only
  - no answer blocks shown

- Failed
  - run returned failed
  - render GovernanceFailurePanel or generic failure panel
  - no answer blocks released

- Error
  - network/server error
  - render frontend error state

## 6. Layout
Three-panel layout:

- left sidebar: FilePanel
- center: ChatThread + EventTimeline + AnswerRenderer
- right side: DrawerShell for Evidence / Debate / Calc inspection

## 7. Component structure
apps/web/src/
- app/
  - layout.tsx
  - page.tsx
  - globals.css
- components/
  - chat/
    - ChatThread.tsx
    - MessageBubble.tsx
    - PromptComposer.tsx
  - files/
    - FilePanel.tsx
    - FileUploader.tsx
    - FileListItem.tsx
  - run/
    - RunStatusBadge.tsx
    - EventStream.tsx
    - EventItem.tsx
  - answer/
    - AnswerRenderer.tsx
    - BlockRegistry.ts
    - DirectAnswerBlock.tsx
    - EvidenceBlock.tsx
    - ConfidenceBlock.tsx
    - DebateSummaryBlock.tsx
    - CalculationBlock.tsx
    - CitationsBlock.tsx
    - ConfidenceBadge.tsx
  - drawers/
    - DrawerShell.tsx
    - EvidenceDrawer.tsx
    - DebateDrawer.tsx
    - CalcTraceDrawer.tsx
  - clarification/
    - ClarificationCard.tsx
    - GovernanceFailurePanel.tsx
- hooks/
  - useRun.ts
  - useFiles.ts
- lib/
  - api.ts
  - types.ts

## 8. Drawer data resolution
Be explicit and exact.

EvidenceDrawer
- source: claim.evidence_refs
- meaning: EvidenceChunk.chunk_id values
- endpoint: GET /api/v1/evidence/chunk/{chunk_id}
- behavior:
  - fetch exact chunk by ID
  - render citation anchor and content
  - support loading / empty / error states

DebateDrawer
- source: RunResult.claims
- endpoint: none required
- behavior:
  - render challenge_flags
  - adjudication_status
  - adjudication_reason
  - claim linkage back to answer blocks

CalcTraceDrawer
- source: claim.calculation_result_ids
- endpoint: GET /api/v1/calculations/{id}/trace
- behavior:
  - render operation
  - trace lines
  - units if present
  - support loading / empty / error states

## 9. File panel behavior
Phase 5 file panel is session-local only.

- file uploads call POST /api/v1/files/upload
- returned FileUploadResponse is stored in React state
- FilePanel renders from session-local state
- refresh clears the list
- no backend list endpoint is assumed in this phase

## 10. Clarification behavior
Clarification is display-only in Phase 5.

- ClarificationCard renders:
  - clarification question
  - reason/context
  - selectable options if available
  - free-text response box
- no resume API call is made in this phase
- this is an inspection and input-capture surface only

## 11. API client
src/lib/api.ts must provide typed wrappers for all frontend-used endpoints:

- uploadFile(file)
- createRun(question, fileIds, userDict?)
- getRun(runId)
- getRunEvents(runId)
- getRunClaims(runId)
- getEvidenceChunk(chunkId)
- retrieveEvidence(query, topK?)
- getCalculation(calcId)
- getCalculationTrace(calcId)
- healthCheck()

## 12. Type contract
TypeScript types in src/lib/types.ts mirror backend Pydantic models manually for this phase.

This is temporary.
Document drift risk clearly.
Preferred future path:
- OpenAPI/Pydantic-driven TS generation

## 13. UI quality requirements
Phase 5 must include:

- drawer loading states
- drawer empty states
- drawer error states
- GovernanceFailurePanel
- keyboard accessibility for primary interactions
- escape-to-close for drawers
- focus management for drawer open/close
- responsive layout behavior for narrower screens

## 14. Tests
Use Vitest + Testing Library.

Required tests:
- AnswerRenderer renders all supported block types
- EventStream renders post-run event timeline
- DrawerShell open/close + Escape behavior
- MessageBubble user vs assistant rendering
- RunStatusBadge all states
- FilePanel empty/loading/populated
- ClarificationCard question/options rendering
- GovernanceFailurePanel blocked-answer rendering
- DebateDrawer rendering from claim data
- EvidenceDrawer loading / error / content states
- CalcTraceDrawer loading / error / content states

## 15. Dependencies
Add:
- tailwindcss ^4
- @tailwindcss/postcss ^4
- postcss ^8
- vitest
- @testing-library/react
- @testing-library/jest-dom
- jsdom

## 16. Environment
Frontend local env:
- NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

Document this in .env.example and keep .env.local gitignored.

## 17. Assumptions
- Tailwind v4 is approved for Phase 5
- backend runs endpoint remains synchronous in Phase 5
- no SSE in Phase 5
- file panel is session-local only
- clarification resume is deferred
- TS types are manually mirrored for now
- block registry pattern is the rendering backbone
- claim.evidence_refs are treated as EvidenceChunk.chunk_id values in Phase 5

## 18. Done definition
Phase 5 is done only if:
- the frontend renders structured typed answer blocks professionally
- drawers resolve exact backend data correctly
- the UI is honest about synchronous execution
- governance failures are rendered clearly
- tests cover core UI states and drawer behaviors
- no analytical logic is embedded in the frontend
