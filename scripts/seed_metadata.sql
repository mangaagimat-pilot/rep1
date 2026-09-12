INSERT INTO ${catalog}.control.ingestion_config
  (source, entity, cdc_enabled, load_type, business_key)
VALUES
  ('Claims', 'Claim', TRUE, 'CDC', 'CLAIM_ID'),
  ('Claims', 'Payment', TRUE, 'CDC', 'PAYMENT_ID'),
  ('Claims', 'MedicalCert', FALSE, 'FULL', 'MED_CERT_ID'),
  ('CRM', 'Customer', FALSE, 'INCREMENTAL', 'CUSTOMER_ID');

INSERT INTO ${catalog}.${schema}.pipeline_audit
VALUES ('seed', 'enterprise_medallion_platform', 'initialized', 0, current_timestamp(), current_timestamp());
