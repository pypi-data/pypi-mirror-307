import json
import time
import uuid
from typing import Any, Dict, List, Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .kafka_config import KafkaConfig

try:

    from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord
    has_connector = True

except Exception:
    AIOKafkaProducer = None
    AIOKafkaConsumer = None
    ConsumerRecord = None
    has_connector = False


class Kafka:
    has_connector=has_connector

    def __init__(self, config: KafkaConfig) -> None:
        self.host = config.host
        self.client_id = config.client_id

        self.metrics_partition = config.metrics_partition
        self.group_id = config.group_id

        self.compression_type = config.compression_type
        self.timeout = config.timeout
        self.enable_idempotence = config.idempotent or True
        self.options: Dict[str, Any] = config.options or {}

        self._client: Union[
            AIOKafkaConsumer,
            None
        ] = None
        self._producer: Union[
            AIOKafkaProducer,
            None
        ] = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):

        self._client = AIOKafkaConsumer(
            bootstrap_servers=self.host,
            client_id=self.client_id,
            group_id=self.group_id,
            request_timeout_ms=self.timeout,
            **self.options
        )

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.host,
            client_id=self.client_id,
            compression_type=self.compression_type,
            request_timeout_ms=self.timeout,
            enable_idempotence=self.enable_idempotence,
            **self.options
        )

        await self._client.start()
        await self._producer.start()

    async def load(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):
        await self._client.subscribe(
            topics=(
                destination_name
            )
        )

        messages: List[ConsumerRecord] = []
        elapsed = 0
        start = time.time()

        async for message in self._client:
            if message.key == metric.name:

                messages.append(message)

            elapsed = time.time() - start

            if elapsed > timeout:
                break

        messages = list(sorted(
            messages,
            key=lambda message: message.timestamp
        ))

        return self._store.parse(
            json.loads(
                messages[-1].value.decode(
                    'utf-8'
                )
            )
        )

    async def send(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):
        
        if self._producer:
            
            batch = self._producer.create_batch()
            batch.append(
                value=metric.json().encode('utf-8'),
                timestamp=metric.timestamp.timestamp(), 
                key=bytes(metric.name, 'utf-8')
            )

            await self._producer.send_batch(
                batch,
                destination_name,
                partition=self.metrics_partition
            )

    async def close(self):
        await self._producer.stop()
