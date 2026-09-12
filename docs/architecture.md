# Enterprise data platform architecture

The bundle implements a source-neutral medallion architecture:

1. **Ingestion** reads landing data through an injectable reader and records a
   cursor in `pipeline_watermark`.
2. **Bronze** preserves source payloads and ingestion metadata.
3. **Silver** cleans records, applies CDC operations, and enforces data quality.
4. **Gold** publishes business aggregates and governed views.

`src/framework` contains runtime-independent contracts for
configuration, structured logging, audit, quality, CDC, ingestion, and retention.
Spark/Databricks adapters can be injected at the notebook or job boundary; the
unit and integration suites therefore run with standard Python only.
