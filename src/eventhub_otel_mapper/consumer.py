"""Azure EventHub Consumer with checkpoint support."""

from __future__ import annotations

import logging
from typing import Any, Callable

from azure.eventhub import EventHubConsumerClient, PartitionContext
from azure.eventhub import EventData

from .config_validator import MappingConfig
from .schema_mapper import SchemaError, map_event

logger = logging.getLogger(__name__)


EventCallback = Callable[[dict[str, Any]], None]


class EventHubConsumer:
    def __init__(
        self,
        connection_string: str,
        eventhub_name: str,
        consumer_group: str,
        config: MappingConfig,
        on_mapped: EventCallback,
        checkpoint_store: Any = None,
    ):
        self._config = config
        self._on_mapped = on_mapped
        self._client = EventHubConsumerClient.from_connection_string(
            connection_string,
            consumer_group=consumer_group,
            eventhub_name=eventhub_name,
            checkpoint_store=checkpoint_store,
        )

    def _handle_event(
        self,
        partition_context: PartitionContext,
        event: EventData,
    ) -> None:
        raw = event.body_as_bytes()
        try:
            mapped = map_event(raw, self._config)
            self._on_mapped(mapped)
        except SchemaError as e:
            logger.error(
                "Schema error in partition %s offset %s: %s",
                partition_context.partition_id,
                event.offset,
                e,
            )
        finally:
            partition_context.update_checkpoint(event)

    def start(self) -> None:
        logger.info("Starting EventHub consumer...")
        with self._client:
            self._client.receive(
                on_event=self._handle_event,
                starting_position="-1",
            )

    def stop(self) -> None:
        self._client.close()
        logger.info("EventHub consumer stopped.")
