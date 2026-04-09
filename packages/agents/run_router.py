"""Run Router agent — decides reuse, hybrid, fresh, or clarification."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import RunMode


class PriorRunSummary(BaseModel):
    """Summary of a prior run for reuse decisions."""

    run_id: UUID
    run_mode: RunMode
    status: str
    question: str | None = None
    scope: str | None = None


class RunRouterInput(BaseModel):
    """Typed input for the Run Router."""

    question: str
    dataset_context: DatasetContext
    prior_runs: list[PriorRunSummary] = Field(default_factory=list)
    available_file_ids: list[UUID] = Field(default_factory=list)
    evidence_chunk_count: int = 0


class RunRouterDecision(BaseModel):
    """Typed output from the Run Router."""

    run_mode: RunMode | None = None
    clarification_required: bool = False
    decision_reason: str = ""


class DeterministicRunRouter(BaseAgent):
    """Rule-based Run Router for tests and local dev."""

    @property
    def agent_name(self) -> str:
        return "run_router"

    def execute(self, *, input: RunRouterInput) -> RunRouterDecision:
        if not input.available_file_ids:
            return RunRouterDecision(
                clarification_required=True,
                decision_reason="No files available; clarification needed",
            )
        if not input.dataset_context.tables:
            return RunRouterDecision(
                clarification_required=True,
                decision_reason="No dataset context; schema clarification needed",
            )
        if input.prior_runs and input.evidence_chunk_count > 0:
            return RunRouterDecision(
                run_mode=RunMode.REUSE,
                decision_reason="Prior runs available with existing evidence",
            )
        if input.evidence_chunk_count > 0:
            return RunRouterDecision(
                run_mode=RunMode.HYBRID,
                decision_reason="Evidence available but no prior runs",
            )
        return RunRouterDecision(
            run_mode=RunMode.FRESH,
            decision_reason="No prior evidence; fresh run required",
        )


class AzureRunRouter(BaseAgent):
    """Azure OpenAI-backed Run Router."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "run_router"

    def execute(self, *, input: RunRouterInput) -> RunRouterDecision:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Run Router for a ministry-grade analytical system. "
                "Decide: reuse, hybrid, fresh, or clarification_required."
            ),
            user_content=input.model_dump_json(),
            response_model=RunRouterDecision,
        )
