"""Storage abstraction contracts for persistence backends."""

from abc import ABC, abstractmethod
from uuid import UUID

from packages.schemas.calculation import CalculationResult
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk


class ChunkRepository(ABC):
    """Abstract contract for persisting and querying evidence chunks."""

    @abstractmethod
    def add_chunks(self, chunks: list[EvidenceChunk]) -> None:
        """Persist a batch of evidence chunks."""

    @abstractmethod
    def get_all(self) -> list[EvidenceChunk]:
        """Return all stored chunks."""

    @abstractmethod
    def get_by_file(self, file_id: UUID) -> list[EvidenceChunk]:
        """Return chunks belonging to a specific file."""

    @abstractmethod
    def count(self) -> int:
        """Total number of stored chunks."""

    @abstractmethod
    def clear(self) -> None:
        """Remove all stored chunks."""


class BundleRepository(ABC):
    """Abstract contract for persisting and retrieving evidence bundles."""

    @abstractmethod
    def save(self, bundle: EvidenceBundle) -> None:
        """Persist an evidence bundle."""

    @abstractmethod
    def get(self, bundle_id: UUID) -> EvidenceBundle | None:
        """Retrieve a bundle by ID, or None if not found."""


class CalculationRepository(ABC):
    """Abstract contract for persisting and retrieving calculation results."""

    @abstractmethod
    def save(self, result: CalculationResult) -> None:
        """Persist a calculation result."""

    @abstractmethod
    def get(self, calculation_id: UUID) -> CalculationResult | None:
        """Retrieve a calculation result by ID, or None if not found."""
