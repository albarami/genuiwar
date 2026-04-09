"""In-memory chunk store for evidence retrieval."""

from uuid import UUID

from packages.schemas.evidence import EvidenceChunk


class ChunkStore:
    """Thread-unsafe in-memory store for parsed evidence chunks.

    Suitable for Phase 2 local development. Will be replaced by a
    persistent backend when the storage layer is built.
    """

    def __init__(self) -> None:
        self._chunks: list[EvidenceChunk] = []
        self._by_file: dict[UUID, list[EvidenceChunk]] = {}

    def add_chunks(self, chunks: list[EvidenceChunk]) -> None:
        """Index a batch of chunks from a parse result."""
        for chunk in chunks:
            self._chunks.append(chunk)
            self._by_file.setdefault(chunk.file_id, []).append(chunk)

    def get_all(self) -> list[EvidenceChunk]:
        """Return every stored chunk."""
        return list(self._chunks)

    def get_by_file(self, file_id: UUID) -> list[EvidenceChunk]:
        """Return chunks belonging to a specific file."""
        return list(self._by_file.get(file_id, []))

    def count(self) -> int:
        """Total number of stored chunks."""
        return len(self._chunks)

    def clear(self) -> None:
        """Remove all stored chunks."""
        self._chunks.clear()
        self._by_file.clear()


chunk_store = ChunkStore()
