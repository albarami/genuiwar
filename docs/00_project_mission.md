# GenUIWar — Project Mission

## Purpose
GenUIWar is a ministry-grade analytical conversation system that lets a user upload files, trigger structured multi-agent analysis, watch the process live, and receive a grounded final answer through a generative UI.

## Core objective
The system must answer questions over uploaded files in a way that is:
- evidence-grounded
- calculation-safe
- transparent in process
- explicit about confidence
- reusable across prior validated runs
- able to launch a fresh targeted run when needed

## What the system must do
1. Accept one or more uploaded files.
2. Parse, normalize, and structure them.
3. Build reusable analytical run outputs.
4. Let the user ask any question at any time.
5. Decide whether to:
   - answer from prior validated outputs,
   - answer from a hybrid of prior outputs plus a targeted run,
   - or launch a fresh deep run.
6. Show the live stream of what the system is doing.
7. Return a final answer in structured generative UI form.

## User experience target
The target experience is a C1-style generative UI:
- conversational chat
- file upload and file management
- live run telemetry
- visible agent actions
- visible debate and adjudication
- evidence and calculation drawers
- structured final answer blocks

## Non-negotiable principles
### No free facts
No important final claim may appear without evidence, verified calculation, or both.

### Accuracy before speed
If the system does not understand the structure, schema, or question intent, it must ask clarifying questions rather than guess.

### Tool-verified numbers
Numeric outputs must come from calculation tools, not model prose.

### Dynamic schema handling
Synthetic data will not match real ministry data. The system must adapt to changing structures, field names, and file layouts.

### Asymmetric agents
Each agent has a narrow role. Intelligence comes from orchestration, challenge, and adjudication, not from making every agent broad.

### Explicit confidence
The system must distinguish direct findings, derived outputs, model-based interpretation, weak signals, and unresolved uncertainty.

## Development posture
The system is being built first without real ministry data.
It must be:
- synthetic-data first
- modular
- adapter-friendly
- auditable
- ready for later ministry integration without redesign

## Success criteria
GenUIWar is successful only if:
1. The user can upload files and ask questions naturally.
2. The system can reuse prior validated outputs honestly.
3. The system can run a fresh question-specific analysis when needed.
4. The user can see meaningful live telemetry.
5. The final answer is evidence-backed and inspectable.
6. Unsupported claims never survive into final output.
7. Calculations are traceable and reliable.
8. Real ministry data can be connected later through adapters.

---
Status: foundational mission file
Use: repository-level source of truth for purpose and constraints
