"""Agent factory — builds agents based on AGENT_MODE config."""

from packages.agents.adjudicator import AzureAdjudicator, DeterministicAdjudicator
from packages.agents.base import BaseAgent
from packages.agents.challenger import AzureChallenger, DeterministicChallenger
from packages.agents.clarification import (
    AzureClarificationAgent,
    DeterministicClarificationAgent,
)
from packages.agents.composer import AzureComposer, DeterministicComposer
from packages.agents.llm_adapter import get_llm_adapter
from packages.agents.primary_analyst import (
    AzurePrimaryAnalyst,
    DeterministicPrimaryAnalyst,
)
from packages.agents.run_router import AzureRunRouter, DeterministicRunRouter
from packages.shared.config import get_settings


class AgentSet:
    """Container for all agent instances needed by the orchestrator."""

    def __init__(
        self,
        *,
        run_router: BaseAgent,
        primary_analyst: BaseAgent,
        challenger: BaseAgent,
        adjudicator: BaseAgent,
        composer: BaseAgent,
        clarification_agent: BaseAgent,
    ) -> None:
        self.run_router = run_router
        self.primary_analyst = primary_analyst
        self.challenger = challenger
        self.adjudicator = adjudicator
        self.composer = composer
        self.clarification_agent = clarification_agent


def build_agents() -> AgentSet:
    """Build agent set based on AGENT_MODE config."""
    mode = get_settings().agent_mode

    if mode == "azure":
        adapter = get_llm_adapter()
        return AgentSet(
            run_router=AzureRunRouter(adapter),
            primary_analyst=AzurePrimaryAnalyst(adapter),
            challenger=AzureChallenger(adapter),
            adjudicator=AzureAdjudicator(adapter),
            composer=AzureComposer(adapter),
            clarification_agent=AzureClarificationAgent(adapter),
        )

    return AgentSet(
        run_router=DeterministicRunRouter(),
        primary_analyst=DeterministicPrimaryAnalyst(),
        challenger=DeterministicChallenger(),
        adjudicator=DeterministicAdjudicator(),
        composer=DeterministicComposer(),
        clarification_agent=DeterministicClarificationAgent(),
    )
