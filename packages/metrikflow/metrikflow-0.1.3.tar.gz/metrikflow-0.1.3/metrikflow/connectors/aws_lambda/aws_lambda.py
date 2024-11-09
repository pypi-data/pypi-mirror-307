import asyncio
import functools
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from metrikflow.connectors.common import ConnectorTypes
from metrikflow.connectors.common.signals import add_signal_handler, handle_loop_stop
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .aws_lambda_config import AWSLambdaConfig

try:
    import boto3
    has_connector=True
except Exception:
    boto3 = None
    has_connector=False


class AWSLambda:
    has_connector=has_connector

    def __init__(self, config: AWSLambdaConfig) -> None:
        self.aws_access_key_id = config.aws_access_key_id
        self.aws_secret_access_key = config.aws_secret_access_key
        self.region_name = config.region_name

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )

        self._client = None
        self._loop = asyncio.get_event_loop()
        self.session_uuid = str(uuid.uuid4())

        self.reporter_type = ConnectorTypes.AWSLambda
        self.reporter_type_name = self.reporter_type.name.capitalize()
        self.metadata_string: str = None

        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):

        add_signal_handler(
            self._loop,
            handle_loop_stop,
            self._executor,
            self._loop
        )

        self._client = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                boto3.client,
                'lambda',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        )

    async def load(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):
        metric_json: Union[str, bytes] = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._client.invoke,
                FunctionName=source_name
            )
        )

        return self._store.parse(metric_json)

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
        
        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._client.invoke,
                FunctionName=destination_name,
                Payload=metric.json()
            )
        )

    async def close(self):
        self._executor.shutdown(cancel_futures=True)
        await self.logger.filesystem.aio['hedra.reporting'].debug(f'{self.metadata_string} - Closing session - {self.session_uuid}')