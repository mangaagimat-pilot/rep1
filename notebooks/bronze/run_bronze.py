from bronze.process_claim import load_to_bronze
from framework.ingestion import IngestionCatalog


def run_bronze(
    source: str,
    entity: str,
    records: list[dict],
    catalog: IngestionCatalog,
    current: list[dict] | None = None,
) -> list[dict]:
    """Load one entity using control.ingestion_config metadata."""

    return load_to_bronze(records, source, entity, catalog, current or [])


if __name__ == "__main__":
    catalog = IngestionCatalog.from_spark_table(spark, "enterprise_prod.control.ingestion_config")
    print(run_bronze(
        "Claims",
        "Claim",
        [{"CLAIM_ID": "claim-1", "operation": "insert", "sequence": 1, "amount": 100}],
        catalog,
    ))
