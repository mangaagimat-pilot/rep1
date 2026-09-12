from gold.fact_national_liability import count_by


def test_claim_pipeline_publishes_aggregate() -> None:
    assert count_by([{"claim_id": "c1"}, {"claim_id": "c1"}], "claim_id") == [
        {"claim_id": "c1", "record_count": 2}
    ]
