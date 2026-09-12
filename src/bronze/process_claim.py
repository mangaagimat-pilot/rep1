from typing import Any, Iterable, Mapping

from framework.ingestion import IngestionBatch, IngestionCatalog, load_from_config
from ingestion.landing_to_bronze import normalize_batch


def to_bronze(batch: IngestionBatch) -> list[dict[str, Any]]:
    return normalize_batch(batch)


def load_to_bronze(
    records: Iterable[Mapping[str, Any]],
    source: str,
    entity: str,
    catalog: IngestionCatalog,
    current: Iterable[Mapping[str, Any]] = (),
) -> list[dict[str, Any]]:
    """Resolve control metadata, apply its load strategy, then add bronze metadata."""

    loaded = load_from_config(source, entity, records, catalog, current)
    return to_bronze(IngestionBatch(source=source, records=loaded))


def deduplicate_bronze(records: Iterable[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    latest: dict[Any, dict[str, Any]] = {}
    without_key: list[dict[str, Any]] = []
    for record in records:
        if key in record:
            latest[record[key]] = dict(record)
        else:
            without_key.append(dict(record))
    return without_key + list(latest.values())

__all__ = ["deduplicate_bronze", "load_to_bronze", "to_bronze"]
