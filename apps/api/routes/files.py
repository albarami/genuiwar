"""File upload and metadata routes."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

from packages.parsers import ParseError, get_parser
from packages.schemas.document import FileDocument
from packages.schemas.enums import FileType
from packages.shared.config import get_settings

router = APIRouter(prefix="/files", tags=["files"])

_ALLOWED_EXTENSIONS: dict[str, FileType] = {
    ".docx": FileType.DOCX,
    ".pdf": FileType.PDF,
    ".pptx": FileType.PPTX,
    ".xlsx": FileType.XLSX,
    ".csv": FileType.CSV,
}

_file_store: dict[UUID, FileUploadResponse] = {}


class FileUploadResponse(BaseModel):
    """Response returned after a successful file upload and parse."""

    file_document: FileDocument
    chunk_count: int
    parse_warnings: list[str]
    metadata: dict[str, Any]


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile) -> FileUploadResponse:
    """Upload a file, validate its type, save it, and parse it.

    Returns the FileDocument metadata plus parse results summary.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    suffix = Path(file.filename).suffix.lower()
    file_type = _ALLOWED_EXTENSIONS.get(suffix)
    if file_type is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: {suffix}. Allowed: {list(_ALLOWED_EXTENSIONS.keys())}",
        )

    settings = get_settings()
    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    content_hash = hashlib.sha256(content).hexdigest()

    file_doc = FileDocument(
        original_filename=file.filename,
        file_type=file_type,
        file_size_bytes=len(content),
        storage_path="",
        content_hash=content_hash,
    )

    save_path = uploads_dir / f"{file_doc.file_id}{suffix}"
    save_path.write_bytes(content)
    file_doc.storage_path = str(save_path)

    try:
        parser = get_parser(file_type)
        result = parser.parse(save_path, file_doc)
    except ParseError as exc:
        raise HTTPException(status_code=422, detail=f"Parse error: {exc.reason}") from exc

    page_count_val = result.metadata.get("page_count")
    if page_count_val is not None:
        file_doc.page_count = int(str(page_count_val))

    sheet_names_val = result.metadata.get("sheet_names")
    if isinstance(sheet_names_val, list):
        file_doc.sheet_names = [str(s) for s in sheet_names_val]

    headers_val = result.metadata.get("headers")
    if headers_val is not None:
        file_doc.detected_schema = {"headers": headers_val}

    response = FileUploadResponse(
        file_document=file_doc,
        chunk_count=len(result.chunks),
        parse_warnings=result.warnings,
        metadata=result.metadata,
    )
    _file_store[file_doc.file_id] = response
    return response


@router.get("/{file_id}", response_model=FileUploadResponse)
async def get_file_metadata(file_id: UUID) -> FileUploadResponse:
    """Retrieve metadata for a previously uploaded file."""
    response = _file_store.get(file_id)
    if response is None:
        raise HTTPException(status_code=404, detail="File not found")
    return response
