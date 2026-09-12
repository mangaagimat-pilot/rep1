CREATE OR REPLACE VIEW ${catalog}.${schema}.vw_claim_summary AS
SELECT claim_id, COUNT(*) AS claim_count
FROM ${catalog}.${schema}.silver_claim
GROUP BY claim_id;
