"""Clarification agent — asks the user when the system cannot proceed safely."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.clarification import ClarificationRequest
from packages.schemas.dataset_context import DatasetContext


class ClarificationInput(BaseModel):
    """Typed input for the Clarification Agent."""

    question: str
    uncertainty_context: str
    dataset_context: DatasetContext
    run_id: UUID


class DeterministicClarificationAgent(BaseAgent):
    """Rule-based Clarification Agent for tests."""

    @property
    def agent_name(self) -> str:
        return "clarification_agent"

    def execute(self, *, input: ClarificationInput) -> ClarificationRequest:
        return ClarificationRequest(
            run_id=input.run_id,
            question=f"Please clarify: {input.uncertainty_context}",
            reason=input.uncertainty_context,
            options=["Option A", "Option B"],
        )


class AzureClarificationAgent(BaseAgent):
    """Azure OpenAI-backed Clarification Agent."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "clarification_agent"

    def execute(self, *, input: ClarificationInput) -> ClarificationRequest:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Clarification Agent. Generate a short, specific, "
                "decision-oriented clarification question. Include schema-specific "
                "questions when identifier meaning or join logic is unclear."
            ),
            user_content=input.model_dump_json(),
            response_model=ClarificationRequest,
        )
