# Privacy Policy: eventhub-otel-mapper

## What I Collect

This tool processes Azure EventHub messages locally and forwards structured telemetry (spans and metrics) to the OTLP endpoint you configure. No data is transmitted to any third-party server outside of your configured backend.

## Data Storage

No data is stored on disk. All processing happens in memory. Checkpoint metadata is written to Azure Blob Storage only if you configure a checkpoint store explicitly.

## Telemetry

This tool does not include any built-in telemetry, crash reporting, or usage tracking.

## Contact

Open a GitHub issue for privacy-related questions.
