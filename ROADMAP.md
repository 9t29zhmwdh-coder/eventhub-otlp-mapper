<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>Roadmap</h1>
</div>

> 🇩🇪 [Deutsche Version](ROADMAP.de.md)

## v0.1 (Current)

- [x] EventHub AMQP consumer with checkpoint support
- [x] JSON, Avro, and Protobuf payload auto-detection
- [x] Declarative YAML field mapping with Pydantic v2 validation
- [x] OpenTelemetry Trace (span) export via OTLP gRPC
- [x] Metric export: counters and histograms via OTLP gRPC
- [x] Azure Monitor / Application Insights exporter integration
- [x] CI on Ubuntu and Windows

## v0.2

- [ ] Avro Schema Registry support (Confluent-compatible)
- [ ] Dead-letter queue (DLQ) routing for schema errors
- [ ] Metric cardinality controls (label allow-list)
- [ ] Docker image and Docker Compose example
- [ ] OTel Collector config example (Prometheus remote write)

## v0.3

- [ ] Multi-EventHub support (fan-in from multiple namespaces)
- [ ] Grafana dashboard template (JSON provisioning)
- [ ] Azure Container Apps deployment manifest
- [ ] Benchmark: events/sec throughput per payload format

## Future

- [ ] Kafka-compatible mode (Azure Event Hubs Kafka surface)
- [ ] Schema drift detection with alerting
- [ ] Entra ID (Managed Identity) authentication without connection strings

---

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Early Release · **Last Updated:** June 2026
