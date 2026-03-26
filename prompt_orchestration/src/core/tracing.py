from __future__ import annotations
from datetime import datetime, timezone
from ..models.models import TraceEvent, Tracer

class InMemoryTracer:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, event: TraceEvent) -> None:
        self.events.append(event)

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

