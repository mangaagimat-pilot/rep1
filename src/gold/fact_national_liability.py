from collections import defaultdict
from typing import Any, Iterable, Mapping


def count_by(records: Iterable[Mapping[str, Any]], dimension: str,
             metric_name: str = "record_count") -> list[dict[str, Any]]:
    counts: dict[Any, int] = defaultdict(int)
    for record in records:
        counts[record.get(dimension)] += 1
    return [{dimension: key, metric_name: value} for key, value in counts.items()]

__all__ = ["count_by"]
