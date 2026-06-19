"""Tests for schema_mapper module."""

import json

import pytest

from eventhub_otel_mapper.config_validator import FieldMapping, MappingConfig
from eventhub_otel_mapper.schema_mapper import (
    MissingFieldError,
    PayloadFormat,
    SchemaError,
    detect_format,
    extract_json,
    map_event,
)


def _make_config(extra: list[dict] | None = None) -> MappingConfig:
    mappings = [
        {"source": "$.correlationId", "target": "span.trace_id"},
        {"source": "$.operation", "target": "span.name"},
        {"source": "$.service", "target": "resource.service.name"},
    ]
    if extra:
        mappings.extend(extra)
    return MappingConfig.model_validate({"version": "1", "mappings": mappings})


def _json_event(**kwargs) -> bytes:
    data = {
        "correlationId": "abc-123",
        "operation": "user.login",
        "service": "auth-service",
    }
    data.update(kwargs)
    return json.dumps(data).encode()


def test_detect_json():
    assert detect_format(_json_event()) == PayloadFormat.json


def test_detect_avro_magic():
    avro_magic = b"\x4f\x62\x6a\x01" + b"\x00" * 10
    assert detect_format(avro_magic) == PayloadFormat.avro


def test_detect_unknown():
    assert detect_format(b"\xff\xfe\xfd\x00") == PayloadFormat.unknown


def test_extract_json_basic():
    cfg = _make_config()
    result = extract_json(_json_event(), cfg.mappings)
    assert result["span.trace_id"] == "abc-123"
    assert result["span.name"] == "user.login"
    assert result["resource.service.name"] == "auth-service"


def test_extract_json_optional_field():
    cfg = _make_config(
        [{"source": "$.severity", "target": "span.attributes.event.severity", "required": False, "default": "INFO"}]
    )
    result = extract_json(_json_event(), cfg.mappings)
    assert result["span.attributes.event.severity"] == "INFO"


def test_extract_json_missing_required():
    cfg = _make_config(
        [{"source": "$.mustExist", "target": "span.attributes.must_exist", "required": True}]
    )
    with pytest.raises(MissingFieldError):
        extract_json(_json_event(), cfg.mappings)


def test_extract_json_invalid_payload():
    cfg = _make_config()
    with pytest.raises(SchemaError, match="Invalid JSON"):
        extract_json(b"not json at all", cfg.mappings)


def test_map_event_json():
    cfg = _make_config()
    result = map_event(_json_event(), cfg)
    assert result["span.name"] == "user.login"


def test_map_event_unknown_format():
    cfg = _make_config()
    with pytest.raises(SchemaError, match="Unknown payload format"):
        map_event(b"\xff\xfe\xfd", cfg)
