import pytest

from silver.process_claim import clean_records, process_silver


def test_silver_cleaning_strips_strings() -> None:
    assert clean_records([{"id": 1, "name": " A "}]) == [{"id": 1, "name": "A"}]


def test_silver_runs_data_quality_checks() -> None:
    records, report = process_silver(
        [{"id": 1, "name": " A "}],
        required=("id",),
        unique_key="id",
    )
    assert records == [{"id": 1, "name": "A"}]
    assert report.passed


def test_silver_rejects_duplicate_business_keys() -> None:
    with pytest.raises(ValueError, match="unique:id"):
        process_silver([{"id": 1}, {"id": 1}], required=("id",), unique_key="id")
