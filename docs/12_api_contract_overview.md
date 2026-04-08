# GenUIWar — API Contract Overview

## Goal
Define the high-level API surface before implementation.

## Main API areas
### 1. Conversations
- create conversation
- get conversation
- list conversations
- add message

### 2. Files
- upload file
- list files
- get file metadata
- delete file
- attach file to conversation

### 3. Runs
- create run
- get run
- list runs for conversation
- rerun
- deepen run
- resume clarification-paused run

### 4. Events
- stream run events
- list run events
- get event details

### 5. Evidence
- get evidence bundle
- get citation details
- inspect evidence anchors

### 6. Claims
- get claim ledger
- inspect claim details
- inspect adjudication outcomes

### 7. Calculations
- get calculation result
- inspect calculation trace

### 8. Clarification
- get clarification request
- submit clarification response

### 9. Answers
- get final answer payload
- get answer render blocks

## Contract principles
- all important outputs must be typed
- all IDs must be stable
- all answer objects must link back to run context
- streaming must support the live UI
- the API must expose reuse/hybrid/fresh mode honestly

---
Status: high-level API contract
Use: pre-implementation API planning reference
