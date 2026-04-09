"""Run event emitter — accumulates typed events during a run."""

from typing import Any
from uuid import UUID

from packages.schemas.enums import EventGroup
from packages.schemas.run import RunEvent


class EventEmitter:
    """Accumulates RunEvent objects during a run execution."""

    def __init__(self, run_id: UUID) -> None:
        self._run_id = run_id
        self._events: list[RunEvent] = []
        self._index = 0

    def emit(
        self,
        event_type: str,
        event_group: EventGroup,
        title: str,
        *,
        agent_name: str | None = None,
        summary: str | None = None,
        payload: dict[str, Any] | None = None,
        is_user_visible: bool = True,
    ) -> RunEvent:
        """Create and record a run event."""
        event = RunEvent(
            run_id=self._run_id,
            event_index=self._index,
            event_type=event_type,
            event_group=event_group,
            agent_name=agent_name,
            title=title,
            summary=summary,
            payload=payload or {},
            is_user_visible=is_user_visible,
        )
        self._events.append(event)
        self._index += 1
        return event

    @property
    def events(self) -> list[RunEvent]:
        """Return all emitted events."""
        return list(self._events)
