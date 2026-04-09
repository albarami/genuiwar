"""In-memory storage implementations — used until Postgres is wired."""

from uuid import UUID

from packages.schemas.answer import FinalAnswerPayload
from packages.schemas.calculation import CalculationResult
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.clarification import ClarificationRequest
from packages.schemas.evidence import EvidenceBundle, EvidenceChunk
from packages.schemas.run import Run, RunEvent
from packages.storage.base import (
    AnswerRepository,
    BundleRepository,
    CalculationRepository,
    ChunkRepository,
    ClaimLedgerRepository,
    ClarificationRepository,
    RunEventRepository,
    RunRepository,
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


class InMemoryRunRepository(RunRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Run] = {}

    def save(self, run: Run) -> None:
        self._store[run.run_id] = run

    def get(self, run_id: UUID) -> Run | None:
        return self._store.get(run_id)

    def list_by_conversation(self, conversation_id: UUID) -> list[Run]:
        return [r for r in self._store.values() if r.conversation_id == conversation_id]


class InMemoryRunEventRepository(RunEventRepository):
    def __init__(self) -> None:
        self._events: list[RunEvent] = []

    def save(self, event: RunEvent) -> None:
        self._events.append(event)

    def list_by_run(self, run_id: UUID) -> list[RunEvent]:
        return sorted(
            [e for e in self._events if e.run_id == run_id],
            key=lambda e: e.event_index,
        )


class InMemoryClaimLedgerRepository(ClaimLedgerRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, ClaimLedgerEntry] = {}

    def save(self, claim: ClaimLedgerEntry) -> None:
        self._store[claim.claim_id] = claim

    def save_many(self, claims: list[ClaimLedgerEntry]) -> None:
        for c in claims:
            self._store[c.claim_id] = c

    def get(self, claim_id: UUID) -> ClaimLedgerEntry | None:
        return self._store.get(claim_id)

    def list_by_run(self, run_id: UUID) -> list[ClaimLedgerEntry]:
        return [c for c in self._store.values() if c.run_id == run_id]


class InMemoryAnswerRepository(AnswerRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, FinalAnswerPayload] = {}

    def save(self, answer: FinalAnswerPayload) -> None:
        self._store[answer.answer_id] = answer

    def get(self, answer_id: UUID) -> FinalAnswerPayload | None:
        return self._store.get(answer_id)


class InMemoryClarificationRepository(ClarificationRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, ClarificationRequest] = {}

    def save(self, request: ClarificationRequest) -> None:
        self._store[request.clarification_id] = request

    def get(self, clarification_id: UUID) -> ClarificationRequest | None:
        return self._store.get(clarification_id)
