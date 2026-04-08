# GenUIWar — First Cursor Build Brief

## Goal
This is the first exact implementation brief for Cursor.

Build only **Phase 0** and **Phase 1**.

Do not build the full system yet.

## Scope
### Phase 0
Create:
- repository skeleton
- apps, packages, infra, tests directories
- initial Python and frontend setup files
- shared typed schemas for:
  - Conversation
  - Message
  - FileDocument
  - EvidenceChunk
  - Run
  - RunEvent
  - ClaimLedgerEntry
  - CalculationResult
  - ClarificationRequest
- initial config loading from environment
- basic README and local startup notes if missing

### Phase 1
Create:
- file upload endpoint
- parser interfaces / contracts
- initial parsers or parser placeholders for:
  - DOCX
  - PDF
  - PPTX
  - XLSX
  - CSV
- normalized evidence object generation
- citation anchor generation
- tests for parser contracts and evidence object creation

## Constraints
- No multi-agent debate yet.
- No final answer generation yet.
- No hidden arithmetic in prose.
- No unsupported claims.
- Use synthetic data only.
- Keep implementation modular.
- Use typed schemas everywhere.
- Write tests for every foundation component.

## Required outputs
1. Repo skeleton
2. Backend app bootstrap
3. Frontend app bootstrap
4. Shared schema package
5. Parser package contracts
6. Basic file upload flow
7. Tests
8. Short implementation summary

## Important rules
- Respect all repository docs and Cursor rules.
- Do not improvise architecture.
- Do not collapse parsing, retrieval, and orchestration into one layer.
- Keep later Azure OpenAI integration behind adapters.

---
Status: first implementation brief
Use: first exact task for Cursor
