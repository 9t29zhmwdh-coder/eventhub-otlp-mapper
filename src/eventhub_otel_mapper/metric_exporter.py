"""Export OpenTelemetry Metrics from mapped EventHub event fields."""

from __future__ import annotations

from typing import Any

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from .config_validator import MetricMapping, MetricType


def build_meter_provider(otlp_endpoint: str, headers: dict[str, str]) -> MeterProvider:
    exporter = OTLPMetricExporter(endpoint=otlp_endpoint, headers=headers)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    return MeterProvider(metric_readers=[reader])


class MetricEmitter:
    def __init__(self, meter: metrics.Meter, metric_mappings: list[MetricMapping]):
        self._counters: dict[str, metrics.Counter] = {}
        self._histograms: dict[str, metrics.Histogram] = {}
        self._gauges: dict[str, metrics.ObservableGauge] = {}
        self._meter = meter
        self._gauge_values: dict[str, float] = {}

        for m in metric_mappings:
            if m.type == MetricType.counter:
                self._counters[m.name] = meter.create_counter(
                    m.name, unit=m.unit, description=m.description
                )
            elif m.type == MetricType.histogram:
                self._histograms[m.name] = meter.create_histogram(
                    m.name, unit=m.unit, description=m.description
                )
            elif m.type == MetricType.gauge:
                name = m.name

                def _observe(options: Any, _n=name) -> list[metrics.Observation]:
                    return [metrics.Observation(self._gauge_values.get(_n, 0))]

                self._gauges[m.name] = meter.create_observable_gauge(
                    m.name,
                    callbacks=[_observe],
                    unit=m.unit,
                    description=m.description,
                )

    def record(
        self,
        mapped: dict[str, Any],
        metric_mappings: list[MetricMapping],
        attributes: dict[str, str] | None = None,
    ) -> None:
        attrs = attributes or {}
        for m in metric_mappings:
            field_name = m.source.lstrip("$.")
            raw_value = mapped.get(f"span.attributes.{field_name}") or mapped.get(
                m.source
            )

            if m.condition == "not_null" and raw_value is None:
                continue

            if raw_value is None:
                if m.type == MetricType.counter and m.condition == "not_null":
                    continue
                raw_value = 0

            try:
                value = float(raw_value)
            except (ValueError, TypeError):
                if m.type == MetricType.counter:
                    value = 1.0
                else:
                    continue

            if m.name in self._counters:
                self._counters[m.name].add(int(value), attrs)
            elif m.name in self._histograms:
                self._histograms[m.name].record(value, attrs)
            elif m.name in self._gauges:
                self._gauge_values[m.name] = value
