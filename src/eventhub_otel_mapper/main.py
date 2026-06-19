"""CLI entry point for EventHub to OpenTelemetry Auto-Mapper."""

from __future__ import annotations

import logging
import os
import signal
import sys
from typing import Any

from opentelemetry import metrics, trace

from .config_validator import load_config
from .consumer import EventHubConsumer
from .metric_exporter import MetricEmitter, build_meter_provider
from .trace_generator import build_tracer_provider, emit_span

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        logger.error("Required environment variable %s is not set.", name)
        sys.exit(1)
    return value


def run() -> None:
    config_path = os.environ.get("MAPPING_CONFIG", "config/mapping.yaml")
    config = load_config(config_path)

    eh_conn = _require_env("EVENTHUB_CONNECTION_STRING")
    eh_name = _require_env("EVENTHUB_NAME")
    eh_group = os.environ.get("EVENTHUB_CONSUMER_GROUP", "$Default")

    otlp_endpoint = _require_env("OTLP_ENDPOINT")
    otlp_headers: dict[str, str] = {}
    if api_key := os.environ.get("OTLP_API_KEY"):
        otlp_headers["api-key"] = api_key

    tracer_provider = build_tracer_provider(otlp_endpoint, otlp_headers)
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer("eventhub-otel-mapper")

    meter_provider = build_meter_provider(otlp_endpoint, otlp_headers)
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter("eventhub-otel-mapper")
    emitter = MetricEmitter(meter, config.metrics)

    def on_mapped(mapped: dict[str, Any]) -> None:
        emit_span(mapped, tracer)
        emitter.record(mapped, config.metrics)

    consumer = EventHubConsumer(
        connection_string=eh_conn,
        eventhub_name=eh_name,
        consumer_group=eh_group,
        config=config,
        on_mapped=on_mapped,
    )

    def _shutdown(sig: int, frame: Any) -> None:
        logger.info("Shutting down...")
        consumer.stop()
        tracer_provider.shutdown()
        meter_provider.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    consumer.start()


if __name__ == "__main__":
    run()
