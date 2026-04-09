"""Primary Analyst agent — drafts answer and creates claim ledger entries."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from packages.agents.base import BaseAgent
from packages.agents.llm_adapter import LLMAdapter
from packages.schemas.calculation import CalculationResult
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import ClaimType, ConfidenceGrade, Materiality, SupportStatus
from packages.schemas.evidence import EvidenceBundle


class AnalystInput(BaseModel):
    """Typed input for the Primary Analyst."""

    question: str
    evidence_bundle: EvidenceBundle
    dataset_context: DatasetContext
    calculation_results: list[CalculationResult] = Field(default_factory=list)
    run_id: UUID


class AnalystOutput(BaseModel):
    """Typed output from the Primary Analyst."""

    draft_answer: str
    claims: list[ClaimLedgerEntry] = Field(default_factory=list)


class DeterministicPrimaryAnalyst(BaseAgent):
    """Rule-based Primary Analyst for tests."""

    @property
    def agent_name(self) -> str:
        return "primary_analyst"

    def execute(self, *, input: AnalystInput) -> AnalystOutput:
        claims: list[ClaimLedgerEntry] = []
        for chunk in input.evidence_bundle.chunks:
            claims.append(
                ClaimLedgerEntry(
                    run_id=input.run_id,
                    claim_text=f"Based on evidence: {chunk.content[:100]}",
                    claim_type=ClaimType.DIRECT,
                    support_status=SupportStatus.SUPPORTED,
                    confidence_grade=ConfidenceGrade.MODERATE,
                    materiality=Materiality.MEDIUM,
                    evidence_refs=[chunk.chunk_id],
                    created_by_agent="primary_analyst",
                )
            )
        if input.calculation_results:
            for calc in input.calculation_results:
                claims.append(
                    ClaimLedgerEntry(
                        run_id=input.run_id,
                        claim_text=f"Calculated: {calc.operation} = {calc.result}",
                        claim_type=ClaimType.DERIVED,
                        support_status=SupportStatus.SUPPORTED,
                        confidence_grade=ConfidenceGrade.HIGH,
                        materiality=Materiality.HIGH,
                        calculation_result_ids=[calc.calculation_id],
                        created_by_agent="primary_analyst",
                    )
                )
        draft = f"Analysis of: {input.question}. Found {len(claims)} claims."
        return AnalystOutput(draft_answer=draft, claims=claims)


class AzurePrimaryAnalyst(BaseAgent):
    """Azure OpenAI-backed Primary Analyst."""

    def __init__(self, adapter: LLMAdapter) -> None:
        self._adapter = adapter

    @property
    def agent_name(self) -> str:
        return "primary_analyst"

    def execute(self, *, input: AnalystInput) -> AnalystOutput:
        return self._adapter.complete_structured(
            system_prompt=(
                "You are the Primary Analyst. Create claims backed by evidence. "
                "Every claim must have evidence_refs or calculation_result_ids. "
                "Respect identifier scoping from the DatasetContext."
            ),
            user_content=input.model_dump_json(),
            response_model=AnalystOutput,
        )
