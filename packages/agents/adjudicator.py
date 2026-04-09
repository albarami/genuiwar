"""Adjudicator agent — approves, downgrades, or rejects claims."""

from __future__ import annotations

from pydantic import BaseModel, Field

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.enums import AdjudicationStatus, ChallengeFlag, SupportStatus


class AdjudicatorInput(BaseModel):
    """Typed input for the Adjudicator."""

    claims: list[ClaimLedgerEntry]


class AdjudicatorOutput(BaseModel):
    """Typed output from the Adjudicator."""

    adjudicated_claims: list[ClaimLedgerEntry] = Field(default_factory=list)


class DeterministicAdjudicator(BaseAgent):
    """Rule-based Adjudicator for tests."""

    @property
    def agent_name(self) -> str:
        return "adjudicator"

    def execute(self, *, input: AdjudicatorInput) -> AdjudicatorOutput:
        results: list[ClaimLedgerEntry] = []
        for claim in input.claims:
            if claim.support_status == SupportStatus.UNSUPPORTED:
                results.append(
                    claim.model_copy(
                        update={
                            "adjudication_status": AdjudicationStatus.REJECTED,
                            "adjudication_reason": "Unsupported claim",
                        }
                    )
                )
            elif ChallengeFlag.MISSING_EVIDENCE in claim.challenge_flags:
                results.append(
                    claim.model_copy(
                        update={
                            "adjudication_status": AdjudicationStatus.REJECTED,
                            "adjudication_reason": "Missing evidence",
                        }
                    )
                )
            elif claim.challenge_flags:
                results.append(
                    claim.model_copy(
                        update={
                            "adjudication_status": AdjudicationStatus.DOWNGRADED,
                            "adjudication_reason": (
                                f"Downgraded due to: "
                                f"{', '.join(str(f) for f in claim.challenge_flags)}"
                            ),
                        }
                    )
                )
            else:
                results.append(
                    claim.model_copy(
                        update={
                            "adjudication_status": AdjudicationStatus.APPROVED,
                            "adjudication_reason": "No issues found",
                        }
                    )
                )
        return AdjudicatorOutput(adjudicated_claims=results)


class AzureAdjudicator(BaseAgent):
    """Azure OpenAI-backed Adjudicator."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "adjudicator"

    def execute(self, *, input: AdjudicatorInput) -> AdjudicatorOutput:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Adjudicator — the final gate before output. "
                "For each claim: approve, downgrade, or reject. "
                "Rejected claims must never enter the final answer. "
                "Provide a clear adjudication_reason for every decision."
            ),
            user_content=input.model_dump_json(),
            response_model=AdjudicatorOutput,
        )
