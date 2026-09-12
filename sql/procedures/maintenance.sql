OPTIMIZE ${catalog}.${schema}.pipeline_audit;
VACUUM ${catalog}.${schema}.pipeline_audit RETAIN 168 HOURS;
