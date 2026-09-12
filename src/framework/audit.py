from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


@dataclass(frozen=True)
class AuditEvent:
    pipeline: str
    stage: str
    status: str
    records: int = 0
    run_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AuditSink(Protocol):
    def write(self, event: AuditEvent) -> None: ...


class InMemoryAuditSink:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def write(self, event: AuditEvent) -> None:
        self.events.append(event)

    def as_dicts(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self.events]


class AuditLogger:
    def __init__(self, sink: AuditSink) -> None:
        self.sink = sink

    def record(self, pipeline: str, stage: str, status: str, records: int = 0,
               run_id: str = "", **details: Any) -> AuditEvent:
        if status not in {"started", "succeeded", "failed", "skipped"}:
            raise ValueError(f"unsupported audit status: {status}")
        event = AuditEvent(pipeline, stage, status, records, run_id, details)
        self.sink.write(event)
        return event
