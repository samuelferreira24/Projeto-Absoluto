from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import uuid


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class WorkState(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Event:
    type: str
    work_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=now_iso)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Work:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: WorkState = WorkState.CREATED
    capability_id: str | None = None
    result: Any = None
    events: list[Event] = field(default_factory=list)
    provenance: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, event_type: str, **payload: Any) -> Event:
        event = Event(event_type, self.id, payload)
        self.events.append(event)
        return event
