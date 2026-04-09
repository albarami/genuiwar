"""Local keyword retriever — scores chunks by keyword overlap."""

import re

from packages.retrieval.base import BaseRetriever, RetrievalFilters
from packages.retrieval.store import ChunkStore
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk


def _tokenize(text: str) -> set[str]:
    """Split text into lowercase alphanumeric tokens."""
    return {t for t in re.split(r"\W+", text.lower()) if t}


def _score(query_tokens: set[str], chunk: EvidenceChunk) -> int:
    """Count how many query tokens appear in the chunk content."""
    chunk_tokens = _tokenize(chunk.content)
    return len(query_tokens & chunk_tokens)


def _apply_filters(
    chunks: list[EvidenceChunk],
    filters: RetrievalFilters | None,
) -> list[EvidenceChunk]:
    """Narrow chunks by metadata filters before scoring."""
    if filters is None:
        return chunks

    result = chunks

    if filters.file_ids is not None:
        allowed = set(filters.file_ids)
        result = [c for c in result if c.file_id in allowed]

    if filters.content_type is not None:
        result = [c for c in result if c.content_type == filters.content_type]

    if filters.sheet_name is not None:
        result = [
            c
            for c in result
            if c.citation_anchor.sheet_name == filters.sheet_name
        ]

    return result


class LocalKeywordRetriever(BaseRetriever):
    """Keyword-based retriever over an in-memory ChunkStore."""

    def __init__(self, store: ChunkStore) -> None:
        self._store = store

    def retrieve(
        self,
        query: str,
        top_k: int,
        filters: RetrievalFilters | None = None,
    ) -> EvidenceBundle:
        """Retrieve top-k chunks by keyword overlap score."""
        candidates = _apply_filters(self._store.get_all(), filters)
        total_candidates = len(candidates)

        query_tokens = _tokenize(query)

        if not query_tokens:
            return EvidenceBundle(
                query=query,
                chunks=[],
                file_ids=[],
                total_candidates=total_candidates,
            )

        scored = [(chunk, _score(query_tokens, chunk)) for chunk in candidates]
        scored.sort(key=lambda pair: pair[1], reverse=True)

        top = [chunk for chunk, sc in scored[:top_k] if sc > 0]
        file_ids = list({c.file_id for c in top})

        return EvidenceBundle(
            query=query,
            chunks=top,
            file_ids=file_ids,
            total_candidates=total_candidates,
        )
