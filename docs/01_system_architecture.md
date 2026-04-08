# GenUIWar — System Architecture

## Objective
Define the target architecture for a ministry-grade analytical system that:
- works first with synthetic data
- remains adaptable to real ministry schemas later
- enforces strict no-free-facts behavior
- can ask clarification questions when needed
- supports visible multi-agent analysis and generative UI rendering

## Top-level architecture
GenUIWar has eight major layers:

1. **Frontend Generative UI**
2. **Backend API**
3. **Run Orchestration Engine**
4. **File Ingestion and Parsing Layer**
5. **Retrieval and Evidence Layer**
6. **Calculation Layer**
7. **Governance and Trust Layer**
8. **Persistence Layer**

## 1. Frontend Generative UI
Responsibilities:
- chat interface
- file upload and file management
- live streaming of run events
- debate viewer
- evidence drawer
- calculation trace drawer
- confidence panel
- structured final answer blocks

The frontend must render structured events and answer payloads. It must not contain analytical logic.

## 2. Backend API
Responsibilities:
- conversation endpoints
- file upload endpoints
- run creation and status endpoints
- event streaming endpoints
- retrieval and answer endpoints
- clarification question endpoints

The backend coordinates services; it should not hide core analytical logic inside routes.

## 3. Run Orchestration Engine
Responsibilities:
- decide reuse vs hybrid vs fresh run
- lock run scope
- invoke agents in order
- emit run events
- handle failure states
- route clarification pauses and resumes
- enforce adjudication before final answer release

This is the execution backbone of the system.

## 4. File Ingestion and Parsing Layer
Responsibilities:
- parse DOCX, PDF, PPTX, XLSX, CSV
- normalize text and tables
- generate evidence chunks
- generate citation anchors
- identify structural ambiguity
- create file metadata objects

Because synthetic data will differ from real ministry data, the parser layer must be schema-tolerant and adapter-friendly.

## 5. Retrieval and Evidence Layer
Responsibilities:
- chunk indexing
- metadata filtering
- evidence bundle creation
- semantic and keyword retrieval abstraction
- support citation and evidence packaging

All final claims must map back to this layer.

## 6. Calculation Layer
Responsibilities:
- arithmetic
- ratios
- comparisons
- grouped totals
- trend calculations
- denominator checks
- calculation traces

No trusted numeric statement may bypass this layer.

## 7. Governance and Trust Layer
Responsibilities:
- no-free-facts enforcement
- claim typing
- confidence grading
- adjudication rules
- clarification policy
- provenance logging
- auditability

This layer must reject unsupported claims even if the prose sounds convincing.

## 8. Persistence Layer
Responsibilities:
- conversations
- messages
- runs
- run events
- evidence bundles
- claim ledgers
- calculation results
- adjudication results
- final answer payloads
- clarification requests

## Dynamic schema strategy
The system must assume:
- synthetic schemas will differ from real ministry schemas
- field names may vary
- file quality may vary
- some files may be partially structured or ambiguous

Therefore the architecture must support:
- schema mapping
- metadata inspection
- dynamic adapters
- clarification prompts to the user
- safe refusal to overclaim

## High-level flow
1. File upload
2. Document preparation run
3. Background analysis run
4. User asks question
5. Run router decides reuse/hybrid/fresh
6. Retrieval + analysis + calculation
7. Challenge + adjudication
8. Final generative UI answer

## Technology posture
Recommended implementation:
- FastAPI backend
- Next.js frontend
- Postgres persistence
- worker process for async jobs
- Azure OpenAI 5.4 runtime via adapter layer
- local-first development
- adapters for later Azure Search / ministry connectors if needed

---
Status: foundational architecture file
Use: source of truth for system boundaries and core layers
