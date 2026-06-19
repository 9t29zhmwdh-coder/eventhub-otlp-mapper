<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>eventhub-otel-mapper</h1>
</div>

> 🇩🇪 [Deutsche Version](README.de.md)

**Automatically map Azure EventHub messages to OpenTelemetry Traces and Metrics. Python, OTLP, zero vendor lock-in.**

Consume events from any Azure EventHub namespace and emit structured OpenTelemetry spans and metrics to Grafana, Application Insights, Prometheus, or any OTLP-compatible backend. Supports JSON, Avro, and Protobuf payloads with declarative field mapping via YAML.

![Python](https://img.shields.io/badge/Python-3.12+-orange?logo=python)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-OTLP-blue?logo=opentelemetry)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Windows-lightgrey?logo=linux)
![License](https://img.shields.io/badge/License-MIT-green)
[![Azure Ready](https://img.shields.io/badge/Azure-Monitor%20%7C%20App%20Insights-blue?logo=microsoftazure)](docs/azure_integration.md)
[![CI](https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper/actions/workflows/ci.yml)

---

## Features

| Feature | Description |
|---|---|
| Multi-format support | JSON, Avro (fastavro), and Protobuf payload auto-detection |
| Declarative mapping | YAML-based field mapping: EventHub field to OTel span attribute or resource label |
| OTLP export | Traces and metrics via gRPC OTLP to any compatible backend |
| Azure Monitor | Native Application Insights exporter, KQL-ready traces |
| Schema validation | Pydantic v2 config validation with clear error messages for missing or malformed schemas |
| Checkpointing | Azure Blob Storage checkpoint support for production multi-consumer deployments |
| CI tested | Ubuntu and Windows matrix with ruff lint and pytest |

---

## Requirements

- Python 3.12+
- Azure EventHub namespace with a **Listen** policy
- OTLP-compatible backend (Grafana Cloud, Azure Monitor, local OTel Collector, Jaeger)

---

## Quick Start

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper.git
cd eventhub-otel-mapper
pip install -e .

cp .env.example .env
# Fill in EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME, OTLP_ENDPOINT

eventhub-otel-mapper
```

Edit `config/mapping.yaml` to map your EventHub payload fields to OpenTelemetry attributes.

## Mapping Example

```yaml
mappings:
  - source: "$.correlationId"
    target: "span.trace_id"
    required: true

  - source: "$.operation"
    target: "span.name"
    required: true

  - source: "$.service"
    target: "resource.service.name"
    required: true

  - source: "$.duration_ms"
    target: "span.attributes.duration_ms"
    required: false
```

See [`config/mapping.yaml`](config/mapping.yaml) for the full reference.

---

## Azure Integration

See [`docs/azure_integration.md`](docs/azure_integration.md) for:
- Connecting to Azure EventHub namespaces
- Application Insights / Azure Monitor setup
- Grafana Cloud OTLP configuration
- KQL queries for Application Insights

---

## Project Structure

```
src/eventhub_otel_mapper/
  consumer.py          EventHub AMQP consumer with checkpointing
  schema_mapper.py     JSON / Avro / Protobuf payload parser
  trace_generator.py   OpenTelemetry span builder
  metric_exporter.py   OTLP metric counter and histogram emitter
  config_validator.py  Pydantic v2 YAML config and schema validation
  main.py              CLI entry point
config/mapping.yaml    Declarative field mapping
examples/              Sample events, traces, and metrics (OTLP JSON)
```

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

---

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Early Release · **Last Updated:** June 2026
