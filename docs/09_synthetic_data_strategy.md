# GenUIWar — Synthetic Data Strategy

## Purpose
Define how synthetic data will be used to build the system before real ministry data is connected.

## Why synthetic data matters
The synthetic environment is not a placeholder; it is a design stress test.

It must simulate:
- clean structures
- messy structures
- partial structures
- contradictory files
- missing fields
- changing schemas
- unclear headings
- ambiguous denominators
- noisy tables
- cross-file inconsistency

## Design rule
Synthetic data should not mirror one rigid schema only.
It must intentionally vary to force dynamic handling.

## Synthetic asset categories
### 1. Clean reference files
Used to validate the happy path.

### 2. Messy files
Used to test parser resilience and clarification triggers.

### 3. Contradictory files
Used to test reviewer challenge and adjudication.

### 4. Ambiguous-schema files
Used to test schema mapping and clarification policy.

### 5. Calculation stress files
Used to test denominator detection, totals, and comparison logic.

## Requirements
The system must:
- adapt to schema variation
- inspect structure dynamically
- ask clarification questions when meaning is unclear
- refuse to overclaim
- remain evidence-based regardless of structure quality

## Output of synthetic strategy
Create reusable generators for:
- DOCX
- PDF-like text structures
- PPTX slide structures
- XLSX/CSV tables
- metadata variants

---
Status: synthetic-data strategy
Use: development and testing foundation before ministry data
