# GenUIWar — Phase 5 Execution Plan (Generative UI)

Generated: 2026-04-09
Branch: `feat/phase5-generative-ui`

---

## Scope

Phase 5 delivers the generative UI per `docs/05_build_phases.md`:
- Chat shell, post-run event timeline, evidence/debate/calc drawers
- Block-based post-run generative rendering via typed block registry
- Structured final answer UI with claim-linked blocks

## Execution model

Synchronous backend + post-run rendering. The UI shows a loading state
while `POST /runs` blocks, then renders the full `RunResult` at once.
No polling. No SSE. No progressive event population.

## Required backend delta

- `ChunkRepository.get_by_id(chunk_id)` added to ABC + in-memory
- `GET /api/v1/evidence/chunk/{chunk_id}` endpoint added
- EvidenceDrawer resolves exact evidence refs via this endpoint

## UI quality

- Drawer loading/empty/error states
- Governance failure panel for failed runs
- Focus management and Escape-to-close for drawers
- Responsive layout (three-panel collapses on narrow viewports)
- Keyboard accessibility for major interactions

## Deferred

- SSE live streaming (future backend work)
- Clarification resume API (display-only in Phase 5)
- Backend file list endpoint (session-local state)
- Auto-generated TypeScript types (manual mirroring for now)

---

Status: Phase 5 execution plan
Use: bounded implementation guide for Phase 5 only
