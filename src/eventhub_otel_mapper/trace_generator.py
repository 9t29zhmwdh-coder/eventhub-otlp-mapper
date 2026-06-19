"""Build OpenTelemetry Spans from mapped EventHub event fields."""

from __future__ import annotations

import time
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import SpanKind, StatusCode


def build_tracer_provider(otlp_endpoint: str, headers: dict[str, str]) -> TracerProvider:
    resource = Resource.create({"service.name": "eventhub-otel-mapper"})
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, headers=headers)
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    return provider


def emit_span(
    mapped: dict[str, Any],
    tracer: trace.Tracer,
    start_time_ns: int | None = None,
    end_time_ns: int | None = None,
) -> None:
    span_name = mapped.get("span.name", "eventhub.event")
    service_name = mapped.get("resource.service.name", "unknown")
    severity = mapped.get("span.attributes.event.severity", "INFO")
    error_desc = mapped.get("span.status.description")
    duration_ms = mapped.get("span.attributes.duration_ms")

    if start_time_ns is None:
        start_time_ns = time.time_ns()
    if end_time_ns is None:
        end_time_ns = start_time_ns + int((duration_ms or 0) * 1_000_000)

    attrs: dict[str, Any] = {
        "event.severity": severity,
        "service.name": service_name,
    }
    for key, val in mapped.items():
        if key.startswith("span.attributes.") and val is not None:
            attr_key = key.removeprefix("span.attributes.")
            attrs[attr_key] = str(val)

    http_status = mapped.get("span.attributes.http.status_code")
    if http_status is not None:
        try:
            attrs["http.status_code"] = int(http_status)
        except (ValueError, TypeError):
            pass

    with tracer.start_as_current_span(
        span_name,
        kind=SpanKind.CONSUMER,
        attributes=attrs,
        start_time=start_time_ns,
    ) as span:
        if error_desc:
            span.set_status(StatusCode.ERROR, error_desc)
        else:
            span.set_status(StatusCode.OK)
        span.end(end_time=end_time_ns)
