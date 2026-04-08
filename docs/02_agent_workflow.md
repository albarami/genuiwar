# GenUIWar — Agent Workflow

## Goal
Define the roles, sequence, and operating rules for the multi-agent system.

## Agent set
### 1. Run Router
Decides whether to:
- reuse prior validated outputs
- perform a hybrid run
- perform a fresh run
- request clarification first

### 2. Ingestion Agent
Parses files, extracts structure, and produces normalized document objects.

### 3. Linking Agent
Builds links across entities, sections, tables, and files.

### 4. Retrieval Agent
Selects the evidence bundle needed for the current question.

### 5. Primary Analyst
Creates the draft analytical answer and the initial claim ledger.

### 6. Calculator Agent
Executes every required trusted calculation.

### 7. Challenger Agent
Operates in **AlMuhasbi** or **Devil’s Advocate** mode to challenge:
- weak logic
- unsupported claims
- shallow synthesis
- denominator issues
- false precision
- contradictions

### 8. Adjudicator Agent
Approves, downgrades, rejects, or sends claims back for clarification.

### 9. Composer Agent
Builds the final structured answer payload using only approved claims.

### 10. Clarification Agent
Generates clarification questions when the system cannot answer safely.

## Workflow after file upload
1. Ingestion Agent parses files.
2. Linking Agent creates anchors and links.
3. Background run creates reusable outputs.
4. Results are stored as run products.

## Workflow after user question
1. Run Router chooses reuse, hybrid, fresh, or clarification.
2. Retrieval Agent selects relevant evidence.
3. Primary Analyst drafts answer and claim ledger.
4. Calculator Agent executes required calculations.
5. Challenger Agent attacks high-materiality claims.
6. Adjudicator Agent decides what survives.
7. Composer Agent builds final answer payload.
8. Frontend renders run stream + final answer.

## Review discipline
High-materiality claims must always be challenged.
No claim may enter final output without:
- source evidence
- verified calculation trace when needed
- adjudicator approval

## Clarification policy at workflow level
If the system cannot safely proceed because of ambiguity, it must pause and ask the user a clarification question rather than guess.

---
Status: foundational workflow file
Use: source of truth for agent sequence and role boundaries
