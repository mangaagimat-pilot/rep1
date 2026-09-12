CREATE TABLE IF NOT EXISTS ${catalog}.${schema}.data_quality_results (
  run_id STRING,
  rule_name STRING,
  passed BOOLEAN,
  failed_records BIGINT,
  evaluated_at TIMESTAMP
) USING DELTA;
