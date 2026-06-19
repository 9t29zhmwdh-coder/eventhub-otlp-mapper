"""Schema detection and field extraction for JSON, Avro, and Protobuf payloads."""

from __future__ import annotations

import json
import struct
from enum import Enum
from typing import Any

from jsonpath_ng import parse as jsonpath_parse

from .config_validator import FieldMapping, MappingConfig


class PayloadFormat(str, Enum):
    json = "json"
    avro = "avro"
    protobuf = "protobuf"
    unknown = "unknown"


class SchemaError(Exception):
    pass


class MissingFieldError(SchemaError):
    pass


def detect_format(data: bytes) -> PayloadFormat:
    # Avro Object Container starts with magic bytes 0x4F 0x62 0x6A 0x01
    if data[:4] == b"\x4f\x62\x6a\x01":
        return PayloadFormat.avro
    # Protobuf schema registry wire format: 0x00 + 4-byte schema ID
    if len(data) > 5 and data[0] == 0x00:
        try:
            struct.unpack(">I", data[1:5])
            return PayloadFormat.protobuf
        except struct.error:
            pass
    try:
        json.loads(data)
        return PayloadFormat.json
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    return PayloadFormat.unknown


def extract_json(data: bytes, mappings: list[FieldMapping]) -> dict[str, Any]:
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as e:
        raise SchemaError(f"Invalid JSON payload: {e}") from e

    result: dict[str, Any] = {}
    for mapping in mappings:
        value = _extract_jsonpath(payload, mapping.source)
        if value is None:
            if mapping.required and mapping.default is None:
                raise MissingFieldError(
                    f"Required field '{mapping.source}' missing in payload"
                )
            value = mapping.default
        result[mapping.target] = value
    return result


def _extract_jsonpath(payload: dict[str, Any], path: str) -> Any:
    if path.startswith("$."):
        matches = jsonpath_parse(path).find(payload)
        return matches[0].value if matches else None
    return payload.get(path)


def extract_avro(data: bytes, mappings: list[FieldMapping]) -> dict[str, Any]:
    try:
        import io

        import fastavro

        reader = fastavro.reader(io.BytesIO(data))
        records = list(reader)
        if not records:
            raise SchemaError("Empty Avro payload")
        payload = records[0]
    except ImportError as e:
        raise SchemaError("fastavro not installed. Run: pip install fastavro") from e
    except Exception as e:
        raise SchemaError(f"Failed to parse Avro payload: {e}") from e

    result: dict[str, Any] = {}
    for mapping in mappings:
        field_name = mapping.source.lstrip("$.")
        value = payload.get(field_name, mapping.default)
        if value is None and mapping.required and mapping.default is None:
            raise MissingFieldError(
                f"Required Avro field '{field_name}' missing in payload"
            )
        result[mapping.target] = value
    return result


def extract_protobuf(
    data: bytes, mappings: list[FieldMapping], descriptor: Any = None
) -> dict[str, Any]:
    if descriptor is None:
        raise SchemaError(
            "Protobuf descriptor required. Provide a compiled .proto descriptor."
        )
    try:
        message = descriptor()
        message.ParseFromString(data[5:])  # skip 5-byte schema registry header
        payload = {
            field.name: getattr(message, field.name)
            for field in message.DESCRIPTOR.fields
        }
    except Exception as e:
        raise SchemaError(f"Failed to parse Protobuf payload: {e}") from e

    result: dict[str, Any] = {}
    for mapping in mappings:
        field_name = mapping.source.lstrip("$.")
        value = payload.get(field_name, mapping.default)
        if value is None and mapping.required and mapping.default is None:
            raise MissingFieldError(
                f"Required Protobuf field '{field_name}' missing"
            )
        result[mapping.target] = value
    return result


def map_event(
    data: bytes, config: MappingConfig, protobuf_descriptor: Any = None
) -> dict[str, Any]:
    fmt = detect_format(data)
    if fmt == PayloadFormat.json:
        return extract_json(data, config.mappings)
    if fmt == PayloadFormat.avro:
        return extract_avro(data, config.mappings)
    if fmt == PayloadFormat.protobuf:
        return extract_protobuf(data, config.mappings, protobuf_descriptor)
    raise SchemaError(f"Unknown payload format (first bytes: {data[:8].hex()})")
