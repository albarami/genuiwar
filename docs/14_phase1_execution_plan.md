# GenUIWar — Phase 1 Execution Plan (File Ingestion)

Generated: 2026-04-09
Branch: `feat/phase1-file-ingestion`

---

## Scope

Phase 1 delivers the file ingestion foundation per `docs/05_build_phases.md`:
- File upload endpoint
- Parsers for DOCX, PDF, PPTX, XLSX, CSV
- Normalization into evidence chunks
- Citation anchor generation
- Synthetic test fixtures
- Tests for all of the above

## Out of scope

- Retrieval / indexing (Phase 2)
- Calculation layer (Phase 3)
- Multi-agent orchestration (Phase 4)
- Generative UI (Phase 5)
- No hidden arithmetic, no unsupported claims

## Deliverables

### 1. Parser contract (`packages/parsers/`)
- `base.py` — `BaseParser` ABC, `ParseResult`, `ParseError`
- `registry.py` — `ParserRegistry` mapping `FileType` to parser

### 2. Parser implementations (`packages/parsers/`)
- `docx_parser.py` — paragraphs, headings, tables; anchors by section
- `pdf_parser.py` — page-by-page text + tables; anchors by page
- `pptx_parser.py` — slide text from shapes; anchors by slide number
- `xlsx_parser.py` — per-sheet with headers; anchors by sheet + row range
- `csv_parser.py` — header detection, row chunking; anchors by row range

### 3. File upload API (`apps/api/routes/files.py`)
- `POST /api/v1/files/upload` — multipart upload, validation, parsing
- `GET /api/v1/files/{file_id}` — file metadata retrieval

### 4. Synthetic fixtures (`packages/synthetic_data/`)
- Clean variants: one per format (DOCX, PDF, PPTX, XLSX, CSV)
- Messy variants: DOCX with missing headings, XLSX with merged cells
- Empty variants: for edge-case testing

### 5. Tests (`tests/unit/`)
- Parser contract compliance
- Per-parser: happy path, empty file, malformed file
- Evidence chunk + citation anchor correctness
- File upload API: valid upload, type rejection

## Schema reuse

Existing `CitationAnchor` fields cover all parser needs:
- `page` — PDF pages, PPTX slides
- `section` — DOCX headings
- `sheet_name` + `row_range` — XLSX sheets, CSV rows

No schema changes required. `EvidenceChunk.content_type` distinguishes "text" vs "table".

## Dependencies added

| Dependency | Purpose | Classification |
|-----------|---------|---------------|
| python-docx | DOCX parsing | Required (Phase 1) |
| pdfplumber | PDF parsing | Required (Phase 1) |
| python-pptx | PPTX parsing | Required (Phase 1) |
| openpyxl | XLSX parsing | Required (Phase 1) |
| python-multipart | FastAPI file upload | Required (Phase 1) |
| reportlab | PDF fixture generation | Dev-only (proposal) |

---

Status: Phase 1 execution plan
Use: bounded implementation guide for Phase 1 only
