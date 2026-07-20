<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>eventhub-otlp-mapper</h1>
</div>

[🇬🇧 English Version](README.md)

**Azure EventHub-Nachrichten automatisch in OpenTelemetry Traces und Metrics umwandeln. Python, OTLP, keine Vendor-Bindung.**

Nachrichten aus einem Azure EventHub-Namespace konsumieren und als strukturierte OpenTelemetry-Spans und Metriken an Grafana, Application Insights, Prometheus oder ein beliebiges OTLP-kompatibles Backend senden. Unterstützt JSON-, Avro- und Protobuf-Payloads mit deklarativem Feld-Mapping per YAML.

[![CI](https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper/actions) ![Azure Ready](https://img.shields.io/badge/Azure-Ready-0078d4?logo=microsoftazure&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-Windows_%7C_Ubuntu-lightgrey) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![AI | Claude Code](https://img.shields.io/badge/AI-Claude_Code-black?logo=anthropic&logoColor=white) ![AI | Copilot](https://img.shields.io/badge/AI-Copilot-black?logo=github&logoColor=white)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/9t29zhmwdh-coder/eventhub-otlp-mapper/badge)](https://securityscorecards.dev/viewer/?uri=github.com/9t29zhmwdh-coder/eventhub-otlp-mapper)

> **So läuft es:** Dies ist ein Kommandozeilen-Prozess, keine Desktop-App und kein Server, mit dem man sich verbindet. `eventhub-otlp-mapper` läuft im Vordergrund (oder unter einem Prozessmanager/systemd-Unit im Produktivbetrieb), liest fortlaufend Events aus deinem EventHub-Namespace und erzeugt daraus OTLP-Spans/Metriken, bis du es stoppst; es gibt keinen Installer und keine grafische Oberfläche.

---

> 🌱 Neu hier? → [Schritt-für-Schritt-Anleitung für Einsteiger](GETTING_STARTED.md)

---

**In der Praxis:** du zeigst den Mapper einmalig auf deinen EventHub-Namespace und einen OTLP-Endpunkt, definierst das Feld-Mapping einmal in `config/mapping.yaml`, und jedes weitere Event wird automatisch zu einem korrekt attributierten OpenTelemetry-Span oder einer Metrik in Grafana/Azure Monitor/Prometheus, ohne Code pro Event.

## Funktionen

| Funktion | Beschreibung |
|---|---|
| Multi-Format-Unterstützung | Automatische Erkennung von JSON-, Avro- und Protobuf-Payloads |
| Deklaratives Mapping | YAML-basiertes Feld-Mapping: EventHub-Feld zu OTel-Span-Attribut oder Resource-Label |
| OTLP-Export | Traces und Metriken via gRPC OTLP an beliebige kompatible Backends |
| Azure Monitor | Nativer Application Insights Exporter, KQL-fähige Traces |
| Schema-Validierung | Pydantic v2 Konfigurationsvalidierung mit klaren Fehlermeldungen |
| Checkpointing | Azure Blob Storage Checkpoint-Unterstützung für Produktiv-Deployments |
| CI getestet | Ubuntu und Windows Matrix mit ruff und pytest |

---

## Voraussetzungen

- Python 3.12+
- Azure EventHub-Namespace mit einer **Listen**-Richtlinie
- OTLP-kompatibles Backend (Grafana Cloud, Azure Monitor, OTel Collector, Jaeger)

---

## Schnellstart

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper.git
cd eventhub-otlp-mapper
pip install -e .

cp .env.example .env
# EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME und OTLP_ENDPOINT eintragen

eventhub-otlp-mapper
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

Siehe [`docs/azure_integration.md`](docs/azure_integration.md) für:
- EventHub-Namespace verbinden
- Application Insights / Azure Monitor einrichten
- Grafana Cloud OTLP konfigurieren
- KQL-Abfragen für Application Insights

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

## Deinstallation / Aufräumen

- `pip uninstall eventhub-otlp-mapper`
- Lokale `.env`-Datei löschen; sie enthält den EventHub-Connection-String und OTLP-/Application-Insights-Zugangsdaten
- Bei genutztem Azure-Blob-Storage-Checkpointing den Checkpoint-Container/die Blobs im Storage-Konto manuell entfernen; der Mapper löscht sie beim Beenden oder bei der Deinstallation nicht

## Roadmap

Siehe [ROADMAP.md](ROADMAP.md).

---

**Autor:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · ![version](https://img.shields.io/github/v/release/9t29zhmwdh-coder/eventhub-otlp-mapper?color=6b7280&style=flat-square) · **Lizenz:** MIT
