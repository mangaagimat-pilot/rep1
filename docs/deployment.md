# Deployment

Validate and deploy with the Databricks CLI:

```powershell
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle deploy -t test
databricks bundle deploy -t prod
```

Azure Pipelines uses the matching `azure-pipelines/deploy-*.yml` definition.
