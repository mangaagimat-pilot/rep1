from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ChangeRecord:
    key: str
    operation: str
    values: Mapping[str, Any]
    sequence: int | datetime


def apply_changes(current: Iterable[Mapping[str, Any]], changes: Iterable[ChangeRecord],
                  key_column: str = "id") -> list[dict[str, Any]]:
    state = {str(row[key_column]): dict(row) for row in current}
    for change in sorted(changes, key=lambda item: item.sequence):
        if change.operation not in {"insert", "update", "delete"}:
            raise ValueError(f"unsupported CDC operation: {change.operation}")
        if change.operation == "delete":
            state.pop(change.key, None)
        else:
            state[change.key] = {key_column: change.key, **dict(change.values)}
    return list(state.values())
