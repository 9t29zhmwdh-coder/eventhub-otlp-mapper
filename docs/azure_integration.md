<div align="center">
  <img src="../RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>Azure Integration Guide</h1>
</div>

> 🇩🇪 [Deutsche Version](azure_integration.de.md)

## Azure Monitor and Application Insights

Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable to enable the Azure Monitor exporter alongside the standard OTLP export.

```bash
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=xxx;IngestionEndpoint=https://..."
```

In `config/mapping.yaml`, enable the Azure Monitor exporter:

```yaml
azure_monitor:
  connection_string: "${APPLICATIONINSIGHTS_CONNECTION_STRING}"
  enabled: true
```

## OTLP Endpoint Options

| Target | Endpoint | Notes |
|---|---|---|
| Grafana Cloud | `https://<stack>.grafana.net/otlp` | Set `Authorization: Basic base64(user:token)` |
| Azure Monitor (OTLP) | `https://dc.services.visualstudio.com/v2.1/track` | Use connection string instead |
| Prometheus (OTel Collector) | `http://localhost:4317` | Requires OTel Collector sidecar |
| Jaeger | `http://localhost:4317` | OTLP gRPC receiver |

## Connecting to an Existing EventHub Namespace

1. Navigate to your EventHub namespace in the Azure Portal
2. Under **Settings > Shared access policies**, create or copy a policy with **Listen** permission
3. Copy the primary connection string
4. Set `EVENTHUB_CONNECTION_STRING` in your environment

```bash
export EVENTHUB_CONNECTION_STRING="Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=Listen;SharedAccessKey=xxx"
export EVENTHUB_NAME="your-eventhub-name"
```

## Checkpoint Store (Production)

For production deployments, use Azure Blob Storage as a checkpoint store to enable multi-consumer scaling:

```python
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

checkpoint_store = BlobCheckpointStore.from_connection_string(
    blob_conn_str, container_name="eventhub-checkpoints"
)
```

Pass `checkpoint_store` to `EventHubConsumer`.

## KQL: Querying Traces in Application Insights

```kql
dependencies
| where cloud_RoleName == "auth-service"
| where name == "user.login"
| summarize avg(duration), count() by bin(timestamp, 5m)
| render timechart
```

```kql
exceptions
| where customDimensions["event.severity"] == "ERROR"
| project timestamp, outerMessage, cloud_RoleName
| order by timestamp desc
```

---

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · **Last Updated:** June 2026
