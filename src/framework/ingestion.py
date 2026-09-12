from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol

from .cdc import ChangeRecord, apply_changes

VALID_LOAD_TYPES = frozenset({"CDC", "FULL", "INCREMENTAL"})


@dataclass(frozen=True)
class SourceSpec:
    name: str
    path: str
    format: str = "json"
    options: dict[str, str] | None = None


@dataclass(frozen=True)
class IngestionBatch:
    source: str
    records: list[dict[str, Any]]
    cursor: str | None = None


@dataclass(frozen=True)
class IngestionConfig:
    """Metadata that determines how one source entity is loaded."""

    source: str
    entity: str
    cdc_enabled: bool
    load_type: str
    business_key: str

    def __post_init__(self) -> None:
        if not self.source.strip() or not self.entity.strip() or not self.business_key.strip():
            raise ValueError("source, entity, and business_key must not be empty")
        load_type = self.load_type.upper()
        if load_type not in VALID_LOAD_TYPES:
            raise ValueError(f"unsupported load_type: {self.load_type}")
        if self.cdc_enabled != (load_type == "CDC"):
            raise ValueError("cdc_enabled must match the CDC load_type")
        object.__setattr__(self, "load_type", load_type)

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> "IngestionConfig":
        cdc = values.get("cdc_enabled", values.get("cdc"))
        if isinstance(cdc, str):
            cdc = cdc.upper() in {"Y", "YES", "TRUE", "1"}
        return cls(
            source=str(values["source"]),
            entity=str(values["entity"]),
            cdc_enabled=bool(cdc),
            load_type=str(values["load_type"]).upper(),
            business_key=str(values["business_key"]),
        )


class IngestionCatalog:
    """In-memory representation of control.ingestion_config for local execution."""

    def __init__(self, configs: Iterable[IngestionConfig]) -> None:
        self._configs = {(config.source, config.entity): config for config in configs}

    def get(self, source: str, entity: str) -> IngestionConfig:
        try:
            return self._configs[(source, entity)]
        except KeyError as exc:
            raise KeyError(f"no ingestion configuration for {source}.{entity}") from exc

    @classmethod
    def from_rows(cls, rows: Iterable[Mapping[str, Any]]) -> "IngestionCatalog":
        return cls(IngestionConfig.from_mapping(row) for row in rows)

    @classmethod
    def from_spark_table(cls, spark: Any, table_name: str) -> "IngestionCatalog":
        """Read control.ingestion_config through a Databricks Spark session."""

        rows = (row.asDict(recursive=True) for row in spark.table(table_name).collect())
        return cls.from_rows(rows)


def load_from_config(
    source: str,
    entity: str,
    records: Iterable[Mapping[str, Any] | ChangeRecord],
    catalog: IngestionCatalog,
    current: Iterable[Mapping[str, Any]] = (),
) -> list[dict[str, Any]]:
    """Load records according to the control metadata for a source entity."""

    config = catalog.get(source, entity)
    if config.load_type == "CDC":
        changes = [
            record if isinstance(record, ChangeRecord) else ChangeRecord(
                key=str(record[config.business_key]),
                operation=str(record["operation"]).lower(),
                values=record,
                sequence=record.get("sequence", index),
            )
            for index, record in enumerate(records)
        ]
        return apply_changes(current, changes, config.business_key)
    loaded = [dict(record) for record in records]
    if config.load_type == "INCREMENTAL":
        latest: dict[Any, dict[str, Any]] = {}
        for record in loaded:
            if config.business_key not in record:
                raise ValueError(f"missing business key {config.business_key} for {source}.{entity}")
            latest[record[config.business_key]] = record
        return list(latest.values())
    return loaded


class IngestionReader(Protocol):
    def read(self, source: SourceSpec, cursor: str | None = None) -> IngestionBatch: ...


class InMemoryIngestionReader:
    def __init__(self, records: Iterable[dict[str, Any]]) -> None:
        self.records = [dict(record) for record in records]

    def read(self, source: SourceSpec, cursor: str | None = None) -> IngestionBatch:
        return IngestionBatch(source.name, list(self.records), cursor=str(len(self.records)))
