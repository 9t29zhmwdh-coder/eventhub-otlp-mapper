"""Config and schema validation using Pydantic v2."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class MetricType(str, Enum):
    counter = "counter"
    histogram = "histogram"
    gauge = "gauge"


class FieldMapping(BaseModel):
    source: str = Field(..., description="JSONPath, Avro, or Protobuf field name")
    target: str = Field(..., description="OTel span or resource attribute key")
    required: bool = True
    default: Any = None

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("source field cannot be empty")
        return v.strip()

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str) -> str:
        allowed_prefixes = ("span.", "resource.", "scope.")
        if not any(v.startswith(p) for p in allowed_prefixes):
            raise ValueError(f"target must start with one of: {allowed_prefixes}")
        return v


class MetricMapping(BaseModel):
    source: str
    name: str
    type: MetricType
    unit: str = ""
    description: str = ""
    condition: str | None = None


class OTLPConfig(BaseModel):
    endpoint: str
    headers: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int = 10

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("OTLP endpoint must start with http:// or https://")
        return v


class AzureMonitorConfig(BaseModel):
    connection_string: str = ""
    enabled: bool = False


class MappingConfig(BaseModel):
    version: str = "1"
    mappings: list[FieldMapping] = Field(default_factory=list)
    metrics: list[MetricMapping] = Field(default_factory=list)
    otlp: OTLPConfig | None = None
    azure_monitor: AzureMonitorConfig = Field(default_factory=AzureMonitorConfig)

    @model_validator(mode="after")
    def check_required_targets(self) -> "MappingConfig":
        required_targets = {"span.trace_id", "span.name", "resource.service.name"}
        present = {m.target for m in self.mappings}
        missing = required_targets - present
        if missing:
            raise ValueError(f"Missing required OTel targets in mappings: {missing}")
        return self


def load_config(path: str) -> MappingConfig:
    import yaml

    with open(path) as f:
        raw = yaml.safe_load(f)
    return MappingConfig.model_validate(raw)
