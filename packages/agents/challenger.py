"""Challenger agent — AlMuhasbi / Devil's Advocate review of claims."""

from __future__ import annotations

from pydantic import BaseModel, Field

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import ChallengeFlag, Materiality
from packages.schemas.evidence import EvidenceBundle


class ChallengerInput(BaseModel):
    """Typed input for the Challenger."""

    claims: list[ClaimLedgerEntry]
    evidence_bundle: EvidenceBundle
    dataset_context: DatasetContext


class ChallengerOutput(BaseModel):
    """Typed output from the Challenger."""

    reviewed_claims: list[ClaimLedgerEntry] = Field(default_factory=list)


class DeterministicChallenger(BaseAgent):
    """Rule-based Challenger for tests — flags high-materiality claims."""

    @property
    def agent_name(self) -> str:
        return "challenger"

    def execute(self, *, input: ChallengerInput) -> ChallengerOutput:
        reviewed: list[ClaimLedgerEntry] = []
        for claim in input.claims:
            flags = list(claim.challenge_flags)
            if claim.materiality == Materiality.HIGH:
                if not claim.evidence_refs:
                    flags.append(ChallengeFlag.MISSING_EVIDENCE)
                if not claim.calculation_result_ids and claim.claim_type == "derived":
                    flags.append(ChallengeFlag.MISSING_CALCULATION_TRACE)
                if not flags:
                    flags.append(ChallengeFlag.WEAK_INTERPRETATION)
            reviewed.append(claim.model_copy(update={"challenge_flags": flags}))
        return ChallengerOutput(reviewed_claims=reviewed)


class AzureChallenger(BaseAgent):
    """Azure OpenAI-backed Challenger — AlMuhasbi mode."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "challenger"

    def execute(self, *, input: ChallengerInput) -> ChallengerOutput:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Challenger operating in AlMuhasbi mode. "
                "Review each claim for: missing evidence, false precision, "
                "denominator issues, schema ambiguity, unsafe joins, "
                "qualitative-as-quantitative mixing. "
                "High-materiality claims MUST have at least one challenge flag."
            ),
            user_content=input.model_dump_json(),
            response_model=ChallengerOutput,
        )
