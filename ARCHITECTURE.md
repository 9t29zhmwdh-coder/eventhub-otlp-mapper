<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>
  <h1>Architecture</h1>
</div>

## Module Layout

```
eventhub-otlp-mapper/
├── src/eventhub_otel_mapper/
│   ├── main.py               Entry point (eventhub-otlp-mapper script): reads .env, starts the consumer loop
│   ├── config_validator.py   Pydantic v2 validation of config/mapping.yaml
│   ├── consumer.py           Azure EventHub consumer client, checkpointing via Blob Storage
│   ├── schema_mapper.py      JSON/Avro/Protobuf payload auto-detection and field extraction via jsonpath-ng
│   ├── trace_generator.py    Maps extracted fields to OpenTelemetry spans
│   └── metric_exporter.py    Maps extracted fields to OpenTelemetry metrics, OTLP gRPC export
├── config/                   Example mapping.yaml files
├── tests/                    pytest test suite
├── examples/                 Programmatic usage examples
└── docs/                     Additional guides
```

## Data Flow

```
Azure EventHub namespace
          |
          v
  consumer.py  (azure-eventhub client, checkpointed via Blob Storage)
          |  Produces: raw event batches
          v
  schema_mapper.py
          |  Detects JSON / Avro / Protobuf, extracts fields per config/mapping.yaml
          |  Validated against config_validator.py (Pydantic v2)
          v
  trace_generator.py  ---->  OpenTelemetry Span
  metric_exporter.py  ---->  OpenTelemetry Metric
          |
          v
  OTLP gRPC exporter (opentelemetry-exporter-otlp-proto-grpc)
  or Azure Monitor exporter (azure-monitor-opentelemetry-exporter)
          |
          v
  Grafana / Application Insights / Prometheus / any OTLP-compatible backend
```

## Key Design Points

- **Declarative mapping**: field-to-attribute mapping lives entirely in `config/mapping.yaml`, no per-event code required. Adding a new EventHub schema means editing the YAML, not the Python.
- **Format auto-detection**: `schema_mapper.py` inspects the payload to decide between JSON, Avro (fastavro) and Protobuf before extraction, so a single consumer instance can handle mixed-format namespaces.
- **Checkpointing**: consumption progress is persisted to Azure Blob Storage so a restarted process resumes from the last processed offset instead of reprocessing the whole partition.

## Adding Support for a New Payload Format

1. Add the format detection logic to `schema_mapper.py`
2. Add a decoder function that returns the same intermediate field-dict shape used by JSON/Avro/Protobuf
3. Add a test in `tests/` with a sample payload of the new format
4. Document the format in the Features table in `README.md`
