CREATE SCHEMA IF NOT EXISTS ${catalog}.${schema};
CREATE SCHEMA IF NOT EXISTS ${catalog}.control;

CREATE TABLE IF NOT EXISTS ${catalog}.control.ingestion_config (
  source STRING NOT NULL,
  entity STRING NOT NULL,
  cdc_enabled BOOLEAN NOT NULL,
  load_type STRING NOT NULL,
  business_key STRING NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp(),
  CONSTRAINT valid_ingestion_load_type CHECK (load_type IN ('CDC', 'FULL', 'INCREMENTAL'))
) USING DELTA;

CREATE TABLE IF NOT EXISTS ${catalog}.${schema}.pipeline_audit (
  run_id STRING,
  pipeline_name STRING,
  status STRING,
  records BIGINT,
  started_at TIMESTAMP,
  completed_at TIMESTAMP
) USING DELTA;
