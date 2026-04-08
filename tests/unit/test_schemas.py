"""Smoke tests for schema validation — ensures all core models instantiate correctly."""

from uuid import uuid4

from packages.schemas import (
    CalculationResult,
    ClaimLedgerEntry,
    ClarificationRequest,
    Conversation,
    EvidenceChunk,
    FileDocument,
    Message,
    Run,
    RunEvent,
)
from packages.schemas.enums import (
    ClaimType,
    EventGroup,
    FileType,
    MessageRole,
    RunCategory,
    RunMode,
)
from packages.schemas.evidence import CitationAnchor


class TestConversation:
    def test_create_conversation(self) -> None:
        conv = Conversation()
        assert conv.conversation_id is not None
        assert conv.file_ids == []

    def test_create_message(self) -> None:
        conv_id = uuid4()
        msg = Message(conversation_id=conv_id, role=MessageRole.USER, content="Hello")
        assert msg.conversation_id == conv_id
        assert msg.role == MessageRole.USER


class TestFileDocument:
    def test_create_file_document(self) -> None:
        doc = FileDocument(
            original_filename="report.xlsx",
            file_type=FileType.XLSX,
            file_size_bytes=1024,
            storage_path="/data/uploads/report.xlsx",
        )
        assert doc.file_id is not None
        assert doc.file_type == FileType.XLSX


class TestEvidenceChunk:
    def test_create_evidence_chunk(self) -> None:
        file_id = uuid4()
        chunk = EvidenceChunk(
            file_id=file_id,
            content="Total workforce: 1,200",
            citation_anchor=CitationAnchor(file_id=file_id, page=3, section="Summary"),
        )
        assert chunk.chunk_id is not None
        assert chunk.citation_anchor.page == 3


class TestRun:
    def test_create_run(self) -> None:
        run = Run(
            conversation_id=uuid4(),
            run_category=RunCategory.QUESTION_ANSWERING,
            run_mode=RunMode.FRESH,
        )
        assert run.run_id is not None
        assert run.status == "queued"

    def test_create_run_event(self) -> None:
        event = RunEvent(
            run_id=uuid4(),
            event_index=0,
            event_type="run.mode_selected",
            event_group=EventGroup.RUN_LIFECYCLE,
            title="Run mode selected",
        )
        assert event.is_user_visible is True


class TestClaimLedgerEntry:
    def test_create_claim(self) -> None:
        claim = ClaimLedgerEntry(
            run_id=uuid4(),
            claim_text="Workforce decreased by 15%",
            claim_type=ClaimType.DERIVED,
        )
        assert claim.adjudication_status == "pending"
        assert claim.support_status == "unsupported"
        assert claim.challenge_flags == []


class TestCalculationResult:
    def test_create_calculation(self) -> None:
        calc = CalculationResult(
            run_id=uuid4(),
            operation="percentage_change",
            inputs={"old": 1000, "new": 850},
            result=-15.0,
            trace=["(850 - 1000) / 1000 * 100 = -15.0"],
        )
        assert calc.result == -15.0
        assert len(calc.trace) == 1


class TestClarificationRequest:
    def test_create_clarification(self) -> None:
        clar = ClarificationRequest(
            run_id=uuid4(),
            question="Which column represents workforce exits?",
            reason="Two columns may both represent exits",
            options=["Column A: Terminations", "Column B: Resignations"],
        )
        assert clar.response is None
        assert len(clar.options) == 2
