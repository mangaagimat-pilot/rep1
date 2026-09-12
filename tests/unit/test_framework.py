from datetime import datetime, timedelta, timezone

import pytest

from framework.audit import AuditLogger, InMemoryAuditSink
from framework.config import EnvironmentConfig
from framework.cdc import ChangeRecord, apply_changes
from framework.data_quality import evaluate, not_null, unique
from framework.retention import RetentionPolicy, expired_records
from framework.ingestion import IngestionCatalog, load_from_config


def test_config_validates_and_exposes_database() -> None:
    config = EnvironmentConfig("dev", "catalog", "schema", "/checkpoints")
    assert config.database == "catalog.schema"


def test_quality_report_detects_null_and_duplicates() -> None:
    report = evaluate([{"id": 1}, {"id": 1}, {"id": None}], [not_null("id"), unique("id")])
    assert not report.passed
    assert {result.name for result in report.results} == {"not_null:id", "unique:id"}


def test_cdc_applies_ordered_updates_and_deletes() -> None:
    changes = [
        ChangeRecord("1", "update", {"name": "new"}, 2),
        ChangeRecord("2", "insert", {"name": "two"}, 1),
        ChangeRecord("1", "delete", {}, 3),
    ]
    assert apply_changes([{"id": "1", "name": "old"}], changes) == [{"id": "2", "name": "two"}]


def test_audit_sink_captures_events() -> None:
    sink = InMemoryAuditSink()
    AuditLogger(sink).record("p", "bronze", "succeeded", records=3)
    assert sink.events[0].records == 3


def test_retention_selects_old_records() -> None:
    now = datetime(2025, 1, 10, tzinfo=timezone.utc)
    rows = [{"_ingested_at": now - timedelta(days=10)}, {"_ingested_at": now}]
    assert len(expired_records(rows, RetentionPolicy("t", 7), now)) == 1


def test_invalid_audit_status_is_rejected() -> None:
    with pytest.raises(ValueError):
        AuditLogger(InMemoryAuditSink()).record("p", "x", "bad")


def test_metadata_drives_cdc_full_and_incremental_loads() -> None:
    catalog = IngestionCatalog.from_rows([
        {"source": "Claims", "entity": "Claim", "cdc": "Y", "load_type": "CDC", "business_key": "CLAIM_ID"},
        {"source": "Claims", "entity": "MedicalCert", "cdc": "N", "load_type": "FULL", "business_key": "MED_CERT_ID"},
        {"source": "CRM", "entity": "Customer", "cdc": "N", "load_type": "INCREMENTAL", "business_key": "CUSTOMER_ID"},
    ])
    assert load_from_config(
        "Claims", "Claim",
        [{"CLAIM_ID": "c1", "operation": "insert", "sequence": 1}],
        catalog,
    ) == [{"CLAIM_ID": "c1", "operation": "insert", "sequence": 1}]
    assert load_from_config("Claims", "MedicalCert", [{"MED_CERT_ID": "m1"}], catalog) == [{"MED_CERT_ID": "m1"}]
    assert load_from_config(
        "CRM", "Customer",
        [{"CUSTOMER_ID": "u1", "name": "old"}, {"CUSTOMER_ID": "u1", "name": "new"}],
        catalog,
    ) == [{"CUSTOMER_ID": "u1", "name": "new"}]
