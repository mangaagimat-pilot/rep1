# Ingestion framework

Ingestion batches carry a source and records, while CDC changes are applied in
sequence order. The framework is runtime-neutral so unit tests can run without
Spark; Databricks jobs provide the runtime adapters.

Load behavior is metadata-driven from `${catalog}.control.ingestion_config`.
The table defines the source, entity, CDC flag, load type, and business key.
`CDC` applies ordered changes, `FULL` preserves the complete batch, and
`INCREMENTAL` keeps the latest row for each configured business key.
