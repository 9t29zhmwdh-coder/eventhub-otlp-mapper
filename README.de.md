<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>eventhub-otel-mapper</h1>
</div>

> 🇬🇧 [English Version](README.md)

**Azure EventHub-Nachrichten automatisch in OpenTelemetry Traces und Metrics umwandeln. Python, OTLP, keine Vendor-Bindung.**

Nachrichten aus einem Azure EventHub-Namespace konsumieren und als strukturierte OpenTelemetry-Spans und Metriken an Grafana, Application Insights, Prometheus oder ein beliebiges OTLP-kompatibles Backend senden. Unterstuetzt JSON-, Avro- und Protobuf-Payloads mit deklarativem Feld-Mapping per YAML.

![Python](https://img.shields.io/badge/Python-3.12+-orange?logo=python)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-OTLP-blue?logo=opentelemetry)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Windows-lightgrey?logo=linux)
![License](https://img.shields.io/badge/License-MIT-green)
[![Azure Ready](https://img.shields.io/badge/Azure-Monitor%20%7C%20App%20Insights-blue?logo=microsoftazure)](docs/azure_integration.md)
[![CI](https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper/actions/workflows/ci.yml)

---

## Funktionen

| Funktion | Beschreibung |
|---|---|
| Multi-Format-Unterstuetzung | Automatische Erkennung von JSON-, Avro- und Protobuf-Payloads |
| Deklaratives Mapping | YAML-basiertes Feld-Mapping: EventHub-Feld zu OTel-Span-Attribut oder Resource-Label |
| OTLP-Export | Traces und Metriken via gRPC OTLP an beliebige kompatible Backends |
| Azure Monitor | Nativer Application Insights Exporter, KQL-faehige Traces |
| Schema-Validierung | Pydantic v2 Konfigurationsvalidierung mit klaren Fehlermeldungen |
| Checkpointing | Azure Blob Storage Checkpoint-Unterstuetzung fuer Produktiv-Deployments |
| CI getestet | Ubuntu und Windows Matrix mit ruff und pytest |

---

## Voraussetzungen

- Python 3.12+
- Azure EventHub-Namespace mit einer **Listen**-Richtlinie
- OTLP-kompatibles Backend (Grafana Cloud, Azure Monitor, OTel Collector, Jaeger)

---

## Schnellstart

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otel-mapper.git
cd eventhub-otel-mapper
pip install -e .

cp .env.example .env
# EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME und OTLP_ENDPOINT eintragen

eventhub-otel-mapper
```

`config/mapping.yaml` anpassen, um Payload-Felder auf OTel-Attribute abzubilden.

## Mapping-Beispiel

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
```

---

## Azure Integration

Siehe [`docs/azure_integration.md`](docs/azure_integration.md) fuer:
- EventHub-Namespace verbinden
- Application Insights / Azure Monitor einrichten
- Grafana Cloud OTLP konfigurieren
- KQL-Abfragen fuer Application Insights

---

## Projektstruktur

```
src/eventhub_otel_mapper/
  consumer.py          EventHub AMQP Consumer mit Checkpointing
  schema_mapper.py     JSON / Avro / Protobuf Parser
  trace_generator.py   OpenTelemetry Span Builder
  metric_exporter.py   OTLP Metrik-Exporter (Counter, Histogram)
  config_validator.py  Pydantic v2 YAML-Konfigurationsvalidierung
  main.py              CLI-Einstiegspunkt
config/mapping.yaml    Deklaratives Feld-Mapping
examples/              Beispiel-Events, Traces und Metriken
```

---

**Autor:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Early Release · **Zuletzt aktualisiert:** Juni 2026
