from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class RetentionPolicy:
    table: str
    days: int
    timestamp_column: str = "_ingested_at"

    def __post_init__(self) -> None:
        if self.days < 1 or not self.table.strip():
            raise ValueError("table must be set and days must be positive")

    def cutoff(self, now: datetime | None = None) -> datetime:
        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)
        return current - timedelta(days=self.days)


def expired_records(records: Iterable[Mapping[str, Any]], policy: RetentionPolicy,
                    now: datetime | None = None) -> list[Mapping[str, Any]]:
    cutoff = policy.cutoff(now)
    expired = []
    for record in records:
        value = record.get(policy.timestamp_column)
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if isinstance(value, datetime) and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value and value < cutoff:
            expired.append(record)
    return expired


def vacuum_sql(policy: RetentionPolicy) -> str:
    return f"VACUUM `{policy.table.replace('`', '')}` RETAIN {policy.days * 24} HOURS"
