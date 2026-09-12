from typing import Any, Iterable, Mapping

from framework.cdc import ChangeRecord, apply_changes
from framework.data_quality import Check, DataQualityReport, evaluate, not_null, unique


def clean_records(records: Iterable[Mapping[str, Any]], required: Iterable[str] = ()) -> list[dict[str, Any]]:
    required_columns = tuple(required)
    return [{key: value.strip() if isinstance(value, str) else value for key, value in record.items()}
            for record in records if all(record.get(column) is not None for column in required_columns)]


def merge_changes(current: Iterable[Mapping[str, Any]], changes: Iterable[ChangeRecord],
                  key_column: str = "id") -> list[dict[str, Any]]:
    return apply_changes(current, changes, key_column)


def validate_silver(
    records: Iterable[Mapping[str, Any]],
    required: Iterable[str] = (),
    unique_key: str | None = None,
    checks: Iterable[Check] = (),
) -> DataQualityReport:
    """Evaluate silver constraints after standardization and before publishing."""

    rows = clean_records(records, required=required)
    quality_checks = [not_null(column) for column in required]
    if unique_key:
        quality_checks.append(unique(unique_key))
    quality_checks.extend(checks)
    report = evaluate(rows, quality_checks)
    report.raise_for_failure()
    return report


def process_silver(
    records: Iterable[Mapping[str, Any]],
    required: Iterable[str] = (),
    unique_key: str | None = None,
    checks: Iterable[Check] = (),
) -> tuple[list[dict[str, Any]], DataQualityReport]:
    """Clean and validate records, returning only data that passed quality checks."""

    cleaned = clean_records(records, required=required)
    report = validate_silver(cleaned, unique_key=unique_key, checks=checks)
    return cleaned, report


__all__ = ["clean_records", "merge_changes", "process_silver", "validate_silver"]
