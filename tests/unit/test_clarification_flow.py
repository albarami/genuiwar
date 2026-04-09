"""Tests for Clarification Agent — clarification request produced."""

from uuid import uuid4

from packages.agents.clarification import ClarificationInput, DeterministicClarificationAgent
from packages.schemas.dataset_context import DatasetContext


class TestDeterministicClarificationAgent:
    def test_produces_clarification_request(self) -> None:
        agent = DeterministicClarificationAgent()
        result = agent.execute(
            input=ClarificationInput(
                question="What is the attrition rate?",
                uncertainty_context="Denominator unclear",
                dataset_context=DatasetContext(),
                run_id=uuid4(),
            )
        )
        assert result.question != ""
        assert result.reason != ""
        assert len(result.options) >= 1

    def test_run_id_preserved(self) -> None:
        rid = uuid4()
        agent = DeterministicClarificationAgent()
        result = agent.execute(
            input=ClarificationInput(
                question="Q?",
                uncertainty_context="Ambiguous",
                dataset_context=DatasetContext(),
                run_id=rid,
            )
        )
        assert result.run_id == rid
