"""Run creation, execution, and inspection API routes."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from apps.api.dependencies import chunk_repo
from packages.agents.adjudicator import DeterministicAdjudicator
from packages.agents.challenger import DeterministicChallenger
from packages.agents.clarification import DeterministicClarificationAgent
from packages.agents.composer import DeterministicComposer
from packages.agents.primary_analyst import DeterministicPrimaryAnalyst
from packages.agents.run_router import DeterministicRunRouter
from packages.calculators import CalculationEngine
from packages.orchestration import RunOrchestrator, RunResult
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import RunCategory, RunMode
from packages.schemas.run import Run, RunEvent
from packages.storage.memory import (
    InMemoryClaimLedgerRepository,
    InMemoryRunEventRepository,
    InMemoryRunRepository,
)

router = APIRouter(prefix="/runs", tags=["runs"])

_run_repo = InMemoryRunRepository()
_event_repo = InMemoryRunEventRepository()
_claim_repo = InMemoryClaimLedgerRepository()
_results: dict[UUID, RunResult] = {}


def _build_orchestrator() -> RunOrchestrator:
    return RunOrchestrator(
        run_router=DeterministicRunRouter(),
        primary_analyst=DeterministicPrimaryAnalyst(),
        challenger=DeterministicChallenger(),
        adjudicator=DeterministicAdjudicator(),
        composer=DeterministicComposer(),
        clarification_agent=DeterministicClarificationAgent(),
        chunk_repo=chunk_repo,
        run_repo=_run_repo,
        calc_engine=CalculationEngine(),
    )


class CreateRunRequest(BaseModel):
    """Request body for creating and executing a run."""

    question: str
    conversation_id: UUID = Field(default_factory=uuid4)
    dataset_context: DatasetContext = Field(default_factory=DatasetContext)


@router.post("", response_model=RunResult)
async def create_run(req: CreateRunRequest) -> RunResult:
    """Create and execute a run."""
    run = Run(
        conversation_id=req.conversation_id,
        run_category=RunCategory.QUESTION_ANSWERING,
        run_mode=RunMode.FRESH,
        question=req.question,
    )

    orchestrator = _build_orchestrator()
    result = orchestrator.execute_run(
        run=run,
        question=req.question,
        dataset_context=req.dataset_context,
    )

    _run_repo.save(result.run)
    for event in result.events:
        _event_repo.save(event)
    _claim_repo.save_many(result.claims)
    _results[run.run_id] = result

    return result


@router.get("/{run_id}", response_model=RunResult)
async def get_run(run_id: UUID) -> RunResult:
    """Get run status and result."""
    result = _results.get(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return result


@router.get("/{run_id}/events", response_model=list[RunEvent])
async def get_run_events(run_id: UUID) -> list[RunEvent]:
    """List run events."""
    events = _event_repo.list_by_run(run_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found")
    return events


@router.get("/{run_id}/claims")
async def get_run_claims(run_id: UUID) -> list[dict]:  # type: ignore[type-arg]
    """Get claim ledger for a run."""
    claims = _claim_repo.list_by_run(run_id)
    if not claims:
        raise HTTPException(status_code=404, detail="No claims found")
    return [c.model_dump(mode="json") for c in claims]
