import asyncio
import functools
import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from metrikflow.connectors.common.signals import add_signal_handler, handle_loop_stop
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .s3_config import S3Config

try:
    import boto3
    has_connector = True

except Exception:
    boto3 = None
    has_connector = False


class S3:
    has_connector=has_connector

    def __init__(self, config: S3Config) -> None:
        self.aws_access_key_id = config.aws_access_key_id
        self.aws_secret_access_key = config.aws_secret_access_key
        self.region_name = config.region_name
        self.buckets_namespace = config.buckets_namespace

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )
        self.client = None
        self._loop = asyncio.get_event_loop()

        self.session_uuid = str(uuid.uuid4())
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

        self.client = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                boto3.client,
                's3',
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
        
        try:
            
            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.client.create_bucket,
                    Bucket=source_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.region_name
                    }
                )
            )

        except Exception:
            pass
    
        metric_json = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self.client.get_object,
                Bucket=source_name,
                Key=f'{metric.name}_{metric.metric_id}'
            )
        )

        return self._store.parse(
            json.loads(metric_json)
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
        try:
            
            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.client.create_bucket,
                    Bucket=destination_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.region_name
                    }
                )
            )

        except Exception:
            pass

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self.client.put_object,
                Bucket=destination_name,
                Key=f'{metric.name}_{metric.metric_id}',
                Body=metric.json()
            )
        )
        
    async def close(self):
        self._executor.shutdown(wait=False, cancel_futures=True)