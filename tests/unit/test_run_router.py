"""Tests for Run Router — mode selection logic."""

from uuid import uuid4

from packages.agents.run_router import (
    DeterministicRunRouter,
    PriorRunSummary,
    RunRouterInput,
)
from packages.schemas.dataset_context import DatasetContext, SourceLocator, TableContext
from packages.schemas.enums import RunMode


def _ctx_with_tables() -> DatasetContext:
    fid = uuid4()
    return DatasetContext(
        tables=[TableContext(table_name="t1", source=SourceLocator(file_id=fid))],
        quantitative_sources=[fid],
    )


class TestDeterministicRunRouter:
    def test_fresh_when_no_evidence(self) -> None:
        router = DeterministicRunRouter()
        result = router.execute(
            input=RunRouterInput(
                question="Q?",
                dataset_context=_ctx_with_tables(),
                available_file_ids=[uuid4()],
            )
        )
        assert result.run_mode == RunMode.FRESH

    def test_reuse_when_prior_runs_and_evidence(self) -> None:
        router = DeterministicRunRouter()
        result = router.execute(
            input=RunRouterInput(
                question="Q?",
                dataset_context=_ctx_with_tables(),
                prior_runs=[
                    PriorRunSummary(
                        run_id=uuid4(), run_mode=RunMode.FRESH, status="completed"
                    )
                ],
                available_file_ids=[uuid4()],
                evidence_chunk_count=10,
            )
        )
        assert result.run_mode == RunMode.REUSE

    def test_hybrid_when_evidence_but_no_prior_runs(self) -> None:
        router = DeterministicRunRouter()
        result = router.execute(
            input=RunRouterInput(
                question="Q?",
                dataset_context=_ctx_with_tables(),
                available_file_ids=[uuid4()],
                evidence_chunk_count=5,
            )
        )
        assert result.run_mode == RunMode.HYBRID

    def test_clarification_when_no_files(self) -> None:
        router = DeterministicRunRouter()
        result = router.execute(
            input=RunRouterInput(
                question="Q?",
                dataset_context=_ctx_with_tables(),
            )
        )
        assert result.clarification_required is True

    def test_clarification_when_no_dataset_context(self) -> None:
        router = DeterministicRunRouter()
        result = router.execute(
            input=RunRouterInput(
                question="Q?",
                dataset_context=DatasetContext(),
                available_file_ids=[uuid4()],
            )
        )
        assert result.clarification_required is True
