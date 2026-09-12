# Enterprise Data Platform

This repository is a Databricks Asset Bundle for a governed bronze/silver/gold
platform. It includes source-neutral Python framework services, Delta SQL
objects, medallion notebooks, jobs, a pipeline, Unity Catalog permissions,
environment configuration, and Azure Pipelines automation. The deployment is organized around the ingestion and medallion processing job.

## Prerequisites

- Databricks CLI  bundle support
- Authentication configured with a Databricks CLI profile or OAuth
- A Databricks workspace URL
- Python 3.10+ for local tests and framework development

## Local validation

The framework deliberately has no Spark dependency, so tests run locally:

```powershell
python -m pytest
python -m compileall -q src scripts
python scripts/local_test.py
```

## Configure a workspace

Replace the placeholder workspace URL when deploying, or pass it as a bundle
variable:

```powershell
databricks bundle validate -t dev -v workspace_host=https://<workspace-url>
```

## Deploy

Deploy to development:

```powershell
databricks bundle deploy -t dev -v workspace_host=https://<workspace-url>
```

Deploy to production:

```powershell
databricks bundle deploy -t prod -v workspace_host=https://<workspace-url>
```

Use a Databricks CLI profile instead of inline credentials when authentication
is not provided by the environment.

## Repository layout

- `src/framework`: config, logging, audit, quality,
  CDC, ingestion, and retention contracts
- `src/ingestion`, `src/bronze`, `src/silver`, `src/gold`: medallion transforms
- `notebooks`: Databricks task entry points
- `resources`: jobs, pipeline, and permissions
- `sql`: Delta DDL, CDC procedure, and governed views
- `config`: common, dev, test, and production settings
- `azure-pipelines`: CI and deployment pipelines

The metadata-driven loader uses `${catalog}.control.ingestion_config`, seeded
by `scripts/seed_metadata.sql`, for Claims Claim/Payment/MedicalCert and CRM
Customer ingestion behavior.
