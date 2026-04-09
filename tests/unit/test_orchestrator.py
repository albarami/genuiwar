"""Tests for RunOrchestrator — full pipeline end-to-end."""

from uuid import uuid4

from packages.agents.adjudicator import DeterministicAdjudicator
from packages.agents.challenger import DeterministicChallenger
from packages.agents.clarification import DeterministicClarificationAgent
from packages.agents.composer import DeterministicComposer
from packages.agents.primary_analyst import DeterministicPrimaryAnalyst
from packages.agents.run_router import DeterministicRunRouter
from packages.calculators import CalculationEngine
from packages.orchestration import RunOrchestrator
from packages.retrieval.local import LocalKeywordRetriever
from packages.schemas.dataset_context import (
    DatasetContext,
    EvidenceSourceType,
    SourceLocator,
    TableContext,
)
from packages.schemas.enums import RunCategory, RunMode, RunStatus
from packages.schemas.evidence import CitationAnchor, EvidenceChunk
from packages.schemas.run import Run
from packages.storage import InMemoryChunkRepository
from packages.storage.memory import InMemoryRunRepository


def _build_orchestrator(
    chunk_repo: InMemoryChunkRepository | None = None,
    run_repo: InMemoryRunRepository | None = None,
) -> RunOrchestrator:
    cr = chunk_repo or InMemoryChunkRepository()
    return RunOrchestrator(
        run_router=DeterministicRunRouter(),
        primary_analyst=DeterministicPrimaryAnalyst(),
        challenger=DeterministicChallenger(),
        adjudicator=DeterministicAdjudicator(),
        composer=DeterministicComposer(),
        clarification_agent=DeterministicClarificationAgent(),
        retriever=LocalKeywordRetriever(cr),
        chunk_repo=cr,
        run_repo=run_repo or InMemoryRunRepository(),
        calc_engine=CalculationEngine(),
    )


def _dataset_ctx() -> DatasetContext:
    fid = uuid4()
    return DatasetContext(
        tables=[
            TableContext(
                table_name="headcount",
                source=SourceLocator(file_id=fid, sheet_name="Sheet1"),
                evidence_type=EvidenceSourceType.QUANTITATIVE,
            )
        ],
        quantitative_sources=[fid],
    )


class TestRunOrchestrator:
    def test_full_pipeline_produces_answer(self) -> None:
        fid = uuid4()
        chunk_repo = InMemoryChunkRepository()
        chunk_repo.add_chunks([
            EvidenceChunk(
                file_id=fid,
                content="Total headcount is 1200",
                citation_anchor=CitationAnchor(file_id=fid),
            )
        ])

        orch = _build_orchestrator(chunk_repo=chunk_repo)
        run = Run(
            conversation_id=uuid4(),
            run_category=RunCategory.QUESTION_ANSWERING,
            run_mode=RunMode.FRESH,
        )
        ctx = _dataset_ctx()
        ctx.quantitative_sources = [fid]

        result = orch.execute_run(run, "What is the headcount?", ctx)

        assert result.answer_payload is not None
        assert len(result.claims) >= 1
        assert len(result.events) >= 5
        assert result.run.status == RunStatus.COMPLETED

    def test_clarification_when_no_files(self) -> None:
        orch = _build_orchestrator()
        run = Run(
            conversation_id=uuid4(),
            run_category=RunCategory.QUESTION_ANSWERING,
            run_mode=RunMode.FRESH,
        )
        result = orch.execute_run(run, "Q?", DatasetContext())

        assert result.clarification_request is not None
        assert result.answer_payload is None
        assert result.run.status == RunStatus.WAITING_FOR_CLARIFICATION

    def test_events_include_lifecycle_bookends(self) -> None:
        fid = uuid4()
        chunk_repo = InMemoryChunkRepository()
        chunk_repo.add_chunks([
            EvidenceChunk(
                file_id=fid,
                content="data",
                citation_anchor=CitationAnchor(file_id=fid),
            )
        ])
        ctx = _dataset_ctx()
        ctx.quantitative_sources = [fid]

        orch = _build_orchestrator(chunk_repo=chunk_repo)
        run = Run(
            conversation_id=uuid4(),
            run_category=RunCategory.QUESTION_ANSWERING,
            run_mode=RunMode.FRESH,
        )
        result = orch.execute_run(run, "Q?", ctx)

        types = [e.event_type for e in result.events]
        assert "run.started" in types
        assert "run.completed" in types

    def test_claim_ledger_created_event_emitted(self) -> None:
        fid = uuid4()
        chunk_repo = InMemoryChunkRepository()
        chunk_repo.add_chunks([
            EvidenceChunk(
                file_id=fid,
                content="evidence",
                citation_anchor=CitationAnchor(file_id=fid),
            )
        ])
        ctx = _dataset_ctx()
        ctx.quantitative_sources = [fid]

        orch = _build_orchestrator(chunk_repo=chunk_repo)
        run = Run(
            conversation_id=uuid4(),
            run_category=RunCategory.QUESTION_ANSWERING,
            run_mode=RunMode.FRESH,
        )
        result = orch.execute_run(run, "Q?", ctx)

        types = [e.event_type for e in result.events]
        assert "analysis.claim_ledger_created" in types
