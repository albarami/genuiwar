# apps/worker

Background job runner for async tasks: file parsing, indexing, deep analysis runs.

Uses ARQ (async Redis queue) for job processing.

## Run locally

```bash
make worker
```
