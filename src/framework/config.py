from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EnvironmentConfig:
    environment: str
    catalog: str
    schema: str
    checkpoint_root: str
    source_root: str = "/mnt/landing"
    retention_days: int = 30

    def __post_init__(self) -> None:
        for name in ("environment", "catalog", "schema", "checkpoint_root", "source_root"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.retention_days < 1:
            raise ValueError("retention_days must be positive")

    @property
    def database(self) -> str:
        return f"{self.catalog}.{self.schema}"

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "EnvironmentConfig":
        return cls(
            environment=str(values["environment"]),
            catalog=str(values["catalog"]),
            schema=str(values["schema"]),
            checkpoint_root=str(values["checkpoint_root"]),
            source_root=str(values.get("source_root", "/mnt/landing")),
            retention_days=int(values.get("retention_days", 30)),
        )


def load_config(values: Mapping[str, object] | None = None) -> EnvironmentConfig:
    source = dict(values or {})
    source.setdefault("environment", os.getenv("PLATFORM_ENV", "dev"))
    source.setdefault("catalog", os.getenv("PLATFORM_CATALOG", "enterprise_dev"))
    source.setdefault("schema", os.getenv("PLATFORM_SCHEMA", "platform"))
    source.setdefault("checkpoint_root", os.getenv("PLATFORM_CHECKPOINT_ROOT", "/tmp/checkpoints"))
    source.setdefault("source_root", os.getenv("PLATFORM_SOURCE_ROOT", "/mnt/landing"))
    source.setdefault("retention_days", os.getenv("PLATFORM_RETENTION_DAYS", "30"))
    return EnvironmentConfig.from_mapping(source)
