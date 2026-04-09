"""Base agent contract for all GenUIWar agents."""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract contract that every agent must implement.

    Each agent subclass defines its own typed execute() signature.
    The base class enforces only the agent_name property.
    """

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Unique name of this agent for event attribution."""
