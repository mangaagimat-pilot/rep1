from framework.cdc import ChangeRecord
from framework.ingestion import IngestionBatch
from bronze.process_claim import to_bronze
from bronze.process_claim import load_to_bronze
from gold.fact_national_liability import count_by
from silver.process_claim import clean_records, merge_changes
from framework.ingestion import IngestionCatalog


def test_medallion_transformations() -> None:
    bronze = to_bronze(IngestionBatch("orders", [{"id": "1", "region": "west"}]))
    silver = clean_records(bronze, required=("id",))
    assert silver[0]["_source"] == "orders"
    assert count_by(silver, "region") == [{"region": "west", "record_count": 1}]


def test_silver_merge() -> None:
    result = merge_changes([{"id": "1", "name": "old"}],
                            [ChangeRecord("1", "update", {"name": "new"}, 1)])
    assert result == [{"id": "1", "name": "new"}]


def test_bronze_resolves_ingestion_strategy_from_metadata() -> None:
    catalog = IngestionCatalog.from_rows([
        {"source": "Claims", "entity": "Claim", "cdc": "Y", "load_type": "CDC", "business_key": "CLAIM_ID"},
    ])
    records = load_to_bronze(
        [{"CLAIM_ID": "c1", "operation": "insert", "sequence": 1}],
        "Claims",
        "Claim",
        catalog,
    )
    assert records[0]["CLAIM_ID"] == "c1"
    assert records[0]["_source"] == "Claims"
