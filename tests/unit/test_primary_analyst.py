"""Tests for Primary Analyst — claim creation and evidence refs."""

from uuid import uuid4

from packages.agents.primary_analyst import AnalystInput, DeterministicPrimaryAnalyst
from packages.schemas.dataset_context import DatasetContext
from packages.schemas.evidence import CitationAnchor, EvidenceBundle, EvidenceChunk


class TestDeterministicPrimaryAnalyst:
    def test_creates_claims_from_evidence(self) -> None:
        fid = uuid4()
        chunk = EvidenceChunk(
            file_id=fid,
            content="Total headcount: 1200",
            citation_anchor=CitationAnchor(file_id=fid),
        )
        bundle = EvidenceBundle(query="Q?", chunks=[chunk], file_ids=[fid], total_candidates=1)
        analyst = DeterministicPrimaryAnalyst()
        result = analyst.execute(
            input=AnalystInput(
                question="Q?",
                evidence_bundle=bundle,
                dataset_context=DatasetContext(),
                run_id=uuid4(),
            )
        )
        assert len(result.claims) >= 1
        assert result.claims[0].evidence_refs == [chunk.chunk_id]
        assert result.claims[0].created_by_agent == "primary_analyst"

    def test_creates_derived_claims_from_calculations(self) -> None:
        from packages.schemas.calculation import CalculationResult

        run_id = uuid4()
        calc = CalculationResult(
            run_id=run_id, operation="add", inputs={"a": 1, "b": 2}, result=3
        )
        analyst = DeterministicPrimaryAnalyst()
        result = analyst.execute(
            input=AnalystInput(
                question="Q?",
                evidence_bundle=EvidenceBundle(query="Q?", total_candidates=0),
                dataset_context=DatasetContext(),
                calculation_results=[calc],
                run_id=run_id,
            )
        )
        derived = [c for c in result.claims if c.claim_type == "derived"]
        assert len(derived) >= 1
        assert calc.calculation_id in derived[0].calculation_result_ids
