from ingestion.landing_to_bronze import run_ingestion
from bronze.process_claim import to_bronze
from silver.process_claim import clean_records


def test_pipeline_runner_without_spark() -> None:
    batch = run_ingestion([{"id": 1, "value": "x"}], source="fixture")
    bronze = to_bronze(batch)
    silver = clean_records(bronze, required=("id",))
    assert len(bronze) == 1
    assert silver[0]["_source"] == "fixture"
