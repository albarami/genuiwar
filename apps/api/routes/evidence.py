"""Evidence retrieval and bundle routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.api.dependencies import bundle_repo, chunk_repo
from packages.retrieval.base import RetrievalFilters
from packages.retrieval.local import LocalKeywordRetriever
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk
from packages.shared.config import get_settings

router = APIRouter(prefix="/evidence", tags=["evidence"])


class RetrieveRequest(BaseModel):
    """Request body for evidence retrieval."""

    query: str
    top_k: int | None = None
    filters: RetrievalFilters | None = None


class RetrieveResponse(BaseModel):
    """Response for a retrieval operation."""

    bundle: EvidenceBundle
    chunk_count: int


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_evidence(req: RetrieveRequest) -> RetrieveResponse:
    """Retrieve evidence chunks matching a keyword query."""
    settings = get_settings()
    top_k = req.top_k or settings.top_k_default
    top_k = min(top_k, settings.top_k_max)

    retriever = LocalKeywordRetriever(chunk_repo)
    bundle = retriever.retrieve(
        query=req.query,
        top_k=top_k,
        filters=req.filters,
    )

    bundle_repo.save(bundle)

    return RetrieveResponse(
        bundle=bundle,
        chunk_count=len(bundle.chunks),
    )


@router.get(
    "/bundle/{bundle_id}",
    response_model=EvidenceBundle,
)
async def get_bundle(bundle_id: UUID) -> EvidenceBundle:
    """Retrieve a previously created evidence bundle by ID."""
    bundle = bundle_repo.get(bundle_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle


@router.get(
    "/chunks/{file_id}",
    response_model=list[EvidenceChunk],
)
async def get_chunks_for_file(file_id: UUID) -> list[EvidenceChunk]:
    """Return all evidence chunks for a specific file."""
    chunks = chunk_repo.get_by_file(file_id)
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No chunks found for this file",
        )
    return chunks
