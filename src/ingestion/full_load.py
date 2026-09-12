from framework.ingestion import IngestionBatch


def full_load(records: list[dict], source: str) -> IngestionBatch:
    return IngestionBatch(source=source, records=[dict(record) for record in records])
