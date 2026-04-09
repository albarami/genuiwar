"""In-memory storage implementations — used until Postgres is wired."""

from uuid import UUID

from packages.schemas.calculation import CalculationResult
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk
from packages.storage.base import (
    BundleRepository,
    CalculationRepository,
    ChunkRepository,
)


class InMemoryChunkRepository(ChunkRepository):
    """In-memory chunk store implementing ChunkRepository."""

    def __init__(self) -> None:
        self._chunks: list[EvidenceChunk] = []
        self._by_file: dict[UUID, list[EvidenceChunk]] = {}

    def add_chunks(self, chunks: list[EvidenceChunk]) -> None:
        for chunk in chunks:
            self._chunks.append(chunk)
            self._by_file.setdefault(chunk.file_id, []).append(chunk)

    def get_all(self) -> list[EvidenceChunk]:
        return list(self._chunks)

    def get_by_file(self, file_id: UUID) -> list[EvidenceChunk]:
        return list(self._by_file.get(file_id, []))

    def count(self) -> int:
        return len(self._chunks)

    def clear(self) -> None:
        self._chunks.clear()
        self._by_file.clear()


class InMemoryBundleRepository(BundleRepository):
    """In-memory bundle store implementing BundleRepository."""

    def __init__(self) -> None:
        self._store: dict[UUID, EvidenceBundle] = {}

    def save(self, bundle: EvidenceBundle) -> None:
        self._store[bundle.bundle_id] = bundle

    def get(self, bundle_id: UUID) -> EvidenceBundle | None:
        return self._store.get(bundle_id)


class InMemoryCalculationRepository(CalculationRepository):
    """In-memory calculation store implementing CalculationRepository."""

    def __init__(self) -> None:
        self._store: dict[UUID, CalculationResult] = {}

    def save(self, result: CalculationResult) -> None:
        self._store[result.calculation_id] = result

    def get(self, calculation_id: UUID) -> CalculationResult | None:
        return self._store.get(calculation_id)
