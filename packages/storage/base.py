"""Storage abstraction contracts for persistence backends."""

from abc import ABC, abstractmethod
from uuid import UUID

from packages.schemas.answer import FinalAnswerPayload
from packages.schemas.calculation import CalculationResult
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.clarification import ClarificationRequest
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk
from packages.schemas.run import Run, RunEvent


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
    def get_by_id(self, chunk_id: UUID) -> EvidenceChunk | None:
        """Return a single chunk by its ID, or None if not found."""

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


class RunRepository(ABC):
    """Abstract contract for persisting runs."""

    @abstractmethod
    def save(self, run: Run) -> None:
        """Persist a run."""

    @abstractmethod
    def get(self, run_id: UUID) -> Run | None:
        """Retrieve a run by ID."""

    @abstractmethod
    def list_by_conversation(self, conversation_id: UUID) -> list[Run]:
        """List runs for a conversation."""


class RunEventRepository(ABC):
    """Abstract contract for persisting run events."""

    @abstractmethod
    def save(self, event: RunEvent) -> None:
        """Persist a run event."""

    @abstractmethod
    def list_by_run(self, run_id: UUID) -> list[RunEvent]:
        """List events for a run, ordered by event_index."""


class ClaimLedgerRepository(ABC):
    """Abstract contract for persisting claim ledger entries."""

    @abstractmethod
    def save(self, claim: ClaimLedgerEntry) -> None:
        """Persist a claim."""

    @abstractmethod
    def save_many(self, claims: list[ClaimLedgerEntry]) -> None:
        """Persist multiple claims."""

    @abstractmethod
    def get(self, claim_id: UUID) -> ClaimLedgerEntry | None:
        """Retrieve a claim by ID."""

    @abstractmethod
    def list_by_run(self, run_id: UUID) -> list[ClaimLedgerEntry]:
        """List claims for a run."""


class AnswerRepository(ABC):
    """Abstract contract for persisting final answer payloads."""

    @abstractmethod
    def save(self, answer: FinalAnswerPayload) -> None:
        """Persist a final answer."""

    @abstractmethod
    def get(self, answer_id: UUID) -> FinalAnswerPayload | None:
        """Retrieve an answer by ID."""


class ClarificationRepository(ABC):
    """Abstract contract for persisting clarification requests."""

    @abstractmethod
    def save(self, request: ClarificationRequest) -> None:
        """Persist a clarification request."""

    @abstractmethod
    def get(self, clarification_id: UUID) -> ClarificationRequest | None:
        """Retrieve a clarification request by ID."""
