"""Postgres-backed repository implementations using SQLAlchemy."""

from uuid import UUID

from sqlalchemy.orm import Session, sessionmaker

from packages.schemas.calculation import CalculationResult
from packages.schemas.evidence import (
    CitationAnchor,
    EvidenceBundle,
    EvidenceChunk,
)
from packages.storage.base import (
    BundleRepository,
    CalculationRepository,
    ChunkRepository,
)
from packages.storage.models import (
    CalculationResultRow,
    EvidenceBundleRow,
    EvidenceChunkRow,
)


class PostgresCalculationRepository(CalculationRepository):
    """Postgres-backed calculation result persistence."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, result: CalculationResult) -> None:
        row = CalculationResultRow(
            calculation_id=result.calculation_id,
            run_id=result.run_id,
            operation=result.operation,
            inputs=result.inputs,
            result=result.result,
            trace=result.trace,
            input_units=result.input_units,
            output_unit=result.output_unit,
            evidence_refs=[str(r) for r in result.evidence_refs],
            created_at=result.created_at,
        )
        with self._session_factory() as session:
            session.merge(row)
            session.commit()

    def get(self, calculation_id: UUID) -> CalculationResult | None:
        with self._session_factory() as session:
            row = session.get(CalculationResultRow, calculation_id)
            if row is None:
                return None
            return CalculationResult(
                calculation_id=row.calculation_id,
                run_id=row.run_id,
                operation=row.operation,
                inputs=row.inputs,
                result=row.result,
                trace=row.trace,
                input_units=row.input_units,
                output_unit=row.output_unit,
                evidence_refs=[UUID(r) for r in row.evidence_refs],
                created_at=row.created_at,
            )


class PostgresChunkRepository(ChunkRepository):
    """Postgres-backed evidence chunk persistence."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def add_chunks(self, chunks: list[EvidenceChunk]) -> None:
        rows = [
            EvidenceChunkRow(
                chunk_id=c.chunk_id,
                file_id=c.file_id,
                content=c.content,
                content_type=c.content_type,
                citation_anchor=c.citation_anchor.model_dump(mode="json"),
                metadata_=c.metadata,
                created_at=c.created_at,
            )
            for c in chunks
        ]
        with self._session_factory() as session:
            session.add_all(rows)
            session.commit()

    def get_all(self) -> list[EvidenceChunk]:
        with self._session_factory() as session:
            rows = session.query(EvidenceChunkRow).all()
            return [self._to_domain(r) for r in rows]

    def get_by_id(self, chunk_id: UUID) -> EvidenceChunk | None:
        with self._session_factory() as session:
            row = session.get(EvidenceChunkRow, chunk_id)
            if row is None:
                return None
            return self._to_domain(row)

    def get_by_file(self, file_id: UUID) -> list[EvidenceChunk]:
        with self._session_factory() as session:
            rows = (
                session.query(EvidenceChunkRow)
                .filter(EvidenceChunkRow.file_id == file_id)
                .all()
            )
            return [self._to_domain(r) for r in rows]

    def count(self) -> int:
        with self._session_factory() as session:
            return session.query(EvidenceChunkRow).count()

    def clear(self) -> None:
        with self._session_factory() as session:
            session.query(EvidenceChunkRow).delete()
            session.commit()

    @staticmethod
    def _to_domain(row: EvidenceChunkRow) -> EvidenceChunk:
        anchor_data = dict(row.citation_anchor)
        if "row_range" in anchor_data and anchor_data["row_range"] is not None:
            anchor_data["row_range"] = tuple(anchor_data["row_range"])
        return EvidenceChunk(
            chunk_id=row.chunk_id,
            file_id=row.file_id,
            content=row.content,
            content_type=row.content_type,
            citation_anchor=CitationAnchor(**anchor_data),
            metadata=row.metadata_,
            created_at=row.created_at,
        )


class PostgresBundleRepository(BundleRepository):
    """Postgres-backed evidence bundle persistence."""

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        chunk_repo: ChunkRepository,
    ) -> None:
        self._session_factory = session_factory
        self._chunk_repo = chunk_repo

    def save(self, bundle: EvidenceBundle) -> None:
        row = EvidenceBundleRow(
            bundle_id=bundle.bundle_id,
            query=bundle.query,
            chunk_ids=[str(c.chunk_id) for c in bundle.chunks],
            file_ids=[str(f) for f in bundle.file_ids],
            total_candidates=bundle.total_candidates,
            created_at=bundle.created_at,
        )
        with self._session_factory() as session:
            session.merge(row)
            session.commit()

    def get(self, bundle_id: UUID) -> EvidenceBundle | None:
        with self._session_factory() as session:
            row = session.get(EvidenceBundleRow, bundle_id)
            if row is None:
                return None

            chunk_ids = [UUID(cid) for cid in row.chunk_ids]
            all_chunks = self._chunk_repo.get_all()
            matched = [c for c in all_chunks if c.chunk_id in chunk_ids]

            return EvidenceBundle(
                bundle_id=row.bundle_id,
                query=row.query,
                chunks=matched,
                file_ids=[UUID(f) for f in row.file_ids],
                total_candidates=row.total_candidates,
                created_at=row.created_at,
            )
