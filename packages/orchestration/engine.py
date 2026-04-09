"""Run orchestration engine — sequences agents through the analytical pipeline."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.adjudicator import (
    AdjudicatorInput,
    AdjudicatorOutput,
)
from packages.agents.challenger import (
    ChallengerInput,
    ChallengerOutput,
)
from packages.agents.clarification import (
    ClarificationInput,
)
from packages.agents.composer import ComposerInput
from packages.agents.primary_analyst import (
    AnalystInput,
    AnalystOutput,
)
from packages.agents.run_router import (
    PriorRunSummary,
    RunRouterInput,
)
from packages.calculators import CalculationEngine
from packages.orchestration.events import EventEmitter
from packages.retrieval.local import LocalKeywordRetriever
from packages.schemas.answer import FinalAnswerPayload
from packages.schemas.claim import ClaimLedgerEntry
from packages.schemas.clarification import ClarificationRequest
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.enums import (
    AdjudicationStatus,
    EventGroup,
    RunStatus,
)
from packages.schemas.run import Run, RunEvent
from packages.storage.base import ChunkRepository, RunRepository


class RunResult(BaseModel):
    """Complete output of a run execution."""

    run: Run
    events: list[RunEvent] = Field(default_factory=list)
    claims: list[ClaimLedgerEntry] = Field(default_factory=list)
    answer_payload: FinalAnswerPayload | None = None
    clarification_request: ClarificationRequest | None = None


class RunOrchestrator:
    """Sequences agents through the analytical pipeline.

    Accepts any object with the correct execute() signature for each role.
    Deterministic and Azure implementations both satisfy this.
    """

    def __init__(
        self,
        *,
        run_router: Any,
        primary_analyst: Any,
        challenger: Any,
        adjudicator: Any,
        composer: Any,
        clarification_agent: Any,
        chunk_repo: ChunkRepository,
        run_repo: RunRepository,
        calc_engine: CalculationEngine,
    ) -> None:
        self._run_router = run_router
        self._analyst = primary_analyst
        self._challenger = challenger
        self._adjudicator = adjudicator
        self._composer = composer
        self._clarification = clarification_agent
        self._chunk_repo = chunk_repo
        self._run_repo = run_repo
        self._calc_engine = calc_engine

    def execute_run(
        self,
        run: Run,
        question: str,
        dataset_context: DatasetContext,
    ) -> RunResult:
        """Execute the full analytical pipeline."""
        emitter = EventEmitter(run.run_id)
        run.status = RunStatus.RUNNING
        run.started_at = datetime.now(tz=UTC)

        emitter.emit(
            "run.started", EventGroup.RUN_LIFECYCLE, "Run started",
            summary=f"Question: {question}",
        )

        prior_runs = self._run_repo.list_by_conversation(run.conversation_id)
        prior_summaries = [
            PriorRunSummary(
                run_id=r.run_id,
                run_mode=r.run_mode,
                status=r.status,
                question=r.question,
                scope=r.scope,
            )
            for r in prior_runs
        ]

        router_input = RunRouterInput(
            question=question,
            dataset_context=dataset_context,
            prior_runs=prior_summaries,
            available_file_ids=dataset_context.quantitative_sources
            + dataset_context.qualitative_sources,
            evidence_chunk_count=self._chunk_repo.count(),
        )
        router_decision = self._run_router.execute(input=router_input)

        emitter.emit(
            "run.mode_selected", EventGroup.RUN_LIFECYCLE, "Run mode selected",
            payload={"decision": router_decision.model_dump()},
        )

        if router_decision.clarification_required:
            clar_input = ClarificationInput(
                question=question,
                uncertainty_context=router_decision.decision_reason,
                dataset_context=dataset_context,
                run_id=run.run_id,
            )
            clar_request = self._clarification.execute(input=clar_input)
            emitter.emit(
                "clarification.requested", EventGroup.CLARIFICATION,
                "Clarification needed",
                agent_name="clarification_agent",
            )
            run.status = RunStatus.WAITING_FOR_CLARIFICATION
            return RunResult(
                run=run,
                events=emitter.events,
                clarification_request=clar_request,
            )

        retriever = LocalKeywordRetriever(self._chunk_repo)
        bundle = retriever.retrieve(query=question, top_k=8)

        emitter.emit(
            "retrieval.bundle_selected", EventGroup.RETRIEVAL,
            "Evidence bundle selected",
            payload={"chunk_count": len(bundle.chunks)},
        )

        analyst_input = AnalystInput(
            question=question,
            evidence_bundle=bundle,
            dataset_context=dataset_context,
            run_id=run.run_id,
        )
        analyst_output: AnalystOutput = self._analyst.execute(input=analyst_input)

        emitter.emit(
            "analysis.draft_completed", EventGroup.ANALYSIS,
            "Draft analysis completed",
            agent_name="primary_analyst",
        )
        emitter.emit(
            "analysis.claim_ledger_created", EventGroup.ANALYSIS,
            "Claim ledger created",
            agent_name="primary_analyst",
            payload={"claim_count": len(analyst_output.claims)},
        )

        challenger_input = ChallengerInput(
            claims=analyst_output.claims,
            evidence_bundle=bundle,
            dataset_context=dataset_context,
        )
        challenger_output: ChallengerOutput = self._challenger.execute(
            input=challenger_input
        )

        emitter.emit(
            "challenge.review_completed", EventGroup.CHALLENGE,
            "Challenge review completed",
            agent_name="challenger",
        )

        adj_input = AdjudicatorInput(claims=challenger_output.reviewed_claims)
        adj_output: AdjudicatorOutput = self._adjudicator.execute(input=adj_input)

        emitter.emit(
            "adjudication.completed", EventGroup.ADJUDICATION,
            "Adjudication completed",
            agent_name="adjudicator",
        )

        for claim in adj_output.adjudicated_claims:
            if claim.adjudication_status == AdjudicationStatus.REJECTED:
                emitter.emit(
                    "adjudication.claim_rejected", EventGroup.ADJUDICATION,
                    f"Claim rejected: {claim.claim_text[:60]}",
                    agent_name="adjudicator",
                    payload={"claim_id": str(claim.claim_id)},
                )

        composable = [
            c for c in adj_output.adjudicated_claims
            if c.adjudication_status in (
                AdjudicationStatus.APPROVED,
                AdjudicationStatus.DOWNGRADED,
            )
        ]

        rejected = [
            c for c in adj_output.adjudicated_claims
            if c.adjudication_status == AdjudicationStatus.REJECTED
        ]

        composer_input = ComposerInput(
            claims=composable,
            run_id=run.run_id,
            question=question,
        )
        answer: FinalAnswerPayload = self._composer.execute(input=composer_input)
        answer.rejected_claim_ids = [c.claim_id for c in rejected]

        emitter.emit(
            "answer.completed", EventGroup.ANSWER_RENDERING,
            "Answer assembled",
            agent_name="composer",
        )

        run.status = RunStatus.COMPLETED
        run.completed_at = datetime.now(tz=UTC)

        emitter.emit(
            "run.completed", EventGroup.RUN_LIFECYCLE, "Run completed",
        )

        return RunResult(
            run=run,
            events=emitter.events,
            claims=adj_output.adjudicated_claims,
            answer_payload=answer,
        )
