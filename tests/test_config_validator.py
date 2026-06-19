"""Tests for config_validator module."""

import pytest
from pydantic import ValidationError

from eventhub_otel_mapper.config_validator import (
    FieldMapping,
    MappingConfig,
    MetricMapping,
    MetricType,
    OTLPConfig,
)


def _base_mappings() -> list[dict]:
    return [
        {"source": "$.correlationId", "target": "span.trace_id"},
        {"source": "$.operation", "target": "span.name"},
        {"source": "$.service", "target": "resource.service.name"},
    ]


def test_field_mapping_valid():
    m = FieldMapping(source="$.correlationId", target="span.trace_id")
    assert m.source == "$.correlationId"
    assert m.required is True


def test_field_mapping_invalid_target():
    with pytest.raises(ValidationError, match="target must start with"):
        FieldMapping(source="$.field", target="invalid.target")


def test_field_mapping_empty_source():
    with pytest.raises(ValidationError, match="source field cannot be empty"):
        FieldMapping(source="   ", target="span.name")


def test_otlp_config_valid():
    cfg = OTLPConfig(endpoint="https://otel.example.com:4317")
    assert cfg.timeout_seconds == 10


def test_otlp_config_invalid_endpoint():
    with pytest.raises(ValidationError, match="must start with"):
        OTLPConfig(endpoint="otel.example.com:4317")


def test_mapping_config_requires_trace_id():
    raw = {
        "version": "1",
        "mappings": [
            {"source": "$.operation", "target": "span.name"},
            {"source": "$.service", "target": "resource.service.name"},
        ],
    }
    with pytest.raises(ValidationError, match="span.trace_id"):
        MappingConfig.model_validate(raw)


def test_mapping_config_valid():
    raw = {"version": "1", "mappings": _base_mappings()}
    cfg = MappingConfig.model_validate(raw)
    assert len(cfg.mappings) == 3


def test_metric_mapping_types():
    m = MetricMapping(
        source="$.duration_ms",
        name="eventhub.event.duration",
        type=MetricType.histogram,
        unit="ms",
    )
    assert m.type == MetricType.histogram
