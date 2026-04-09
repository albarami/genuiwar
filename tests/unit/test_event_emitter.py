"""Tests for EventEmitter — all event types emitted correctly."""

from uuid import uuid4

from packages.orchestration.events import EventEmitter
from packages.schemas.enums import EventGroup


class TestEventEmitter:
    def test_emit_creates_event(self) -> None:
        emitter = EventEmitter(uuid4())
        event = emitter.emit("run.started", EventGroup.RUN_LIFECYCLE, "Run started")
        assert event.event_type == "run.started"
        assert event.event_group == EventGroup.RUN_LIFECYCLE

    def test_events_indexed_sequentially(self) -> None:
        emitter = EventEmitter(uuid4())
        e1 = emitter.emit("run.started", EventGroup.RUN_LIFECYCLE, "Start")
        e2 = emitter.emit("run.mode_selected", EventGroup.RUN_LIFECYCLE, "Mode")
        assert e1.event_index == 0
        assert e2.event_index == 1

    def test_events_collected(self) -> None:
        emitter = EventEmitter(uuid4())
        emitter.emit("run.started", EventGroup.RUN_LIFECYCLE, "Start")
        emitter.emit("answer.completed", EventGroup.ANSWER_RENDERING, "Done")
        assert len(emitter.events) == 2

    def test_agent_name_included(self) -> None:
        emitter = EventEmitter(uuid4())
        event = emitter.emit(
            "analysis.draft_completed",
            EventGroup.ANALYSIS,
            "Draft done",
            agent_name="primary_analyst",
        )
        assert event.agent_name == "primary_analyst"

    def test_payload_included(self) -> None:
        emitter = EventEmitter(uuid4())
        event = emitter.emit(
            "retrieval.bundle_selected",
            EventGroup.RETRIEVAL,
            "Bundle selected",
            payload={"chunk_count": 5},
        )
        assert event.payload["chunk_count"] == 5

    def test_run_id_propagated(self) -> None:
        rid = uuid4()
        emitter = EventEmitter(rid)
        event = emitter.emit("run.started", EventGroup.RUN_LIFECYCLE, "Start")
        assert event.run_id == rid
