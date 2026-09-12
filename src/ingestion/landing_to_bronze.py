from datetime import datetime, timezone
from typing import Any, Iterable

from framework.ingestion import IngestionBatch


def run_ingestion(records: Iterable[dict[str, Any]], source: str) -> IngestionBatch:
    return IngestionBatch(source=source, records=[dict(record) for record in records])


def normalize_batch(batch: IngestionBatch) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    return [{**record, "_source": batch.source, "_ingested_at": timestamp}
            for record in batch.records]

__all__ = ["normalize_batch", "run_ingestion"]
