import json
import uuid
from typing import Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .redis_config import RedisConfig

try:

    import aioredis
    has_connector = True

except Exception:
    aioredis = None
    has_connector = True


class Redis:
    has_connector=has_connector

    def __init__(self, config: RedisConfig) -> None:
        self.host = config.host
        self.base = 'rediss' if config.secure else 'redis'
        self.username = config.username
        self.password = config.password
        self.database = config.database

        self.connection = None
        self.pubsub = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):
        self.connection = await aioredis.from_url(
            f'{self.base}://{self.host}',
            username=self.username,
            password=self.password,
            db=self.database
        )

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
        data = await self.connection.get(f'{destination_name}_{metric.name}')
        return self._store.parse(
            json.loads(data)
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
        await self.connection.set(
            f'{destination_name}_{metric.name}',
            metric.json()
        )

    async def close(self):
        await self.connection.close()
