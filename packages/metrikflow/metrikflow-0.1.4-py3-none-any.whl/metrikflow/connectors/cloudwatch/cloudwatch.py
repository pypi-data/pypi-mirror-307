import asyncio
import datetime
import functools
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from metrikflow.connectors.common.signals import add_signal_handler, handle_loop_stop
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate

from .cloudwatch_config import CloudwatchConfig

try:
    import boto3
    has_connector = True

except Exception:
    boto3 = None
    has_connector = False
    

class Cloudwatch:
    has_connector=has_connector

    def __init__(self, config: CloudwatchConfig) -> None:
        self.aws_access_key_id = config.aws_access_key_id
        self.aws_secret_access_key = config.aws_secret_access_key
        self.region_name = config.region_name
        self.iam_role_arn = config.iam_role_arn
        self.schedule_rate = config.schedule_rate

        self.cloudwatch_targets = config.cloudwatch_targets
        self.aws_resource_arns = config.aws_resource_arns
        self.submit_timeout = config.submit_timeout

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )

        self.experiments_rule = None

        self.client = None
        self._loop = asyncio.get_event_loop()

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
                'events',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
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
        raise Exception('Err. - CloudWatch connector is send only.')

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
        await asyncio.wait_for(
            self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.client.put_events,
                    Entries=[
                        {
                            'Time': datetime.datetime.now(
                                datetime.timezone.utc
                            ),
                            'Detail': metric.json(),
                            'DetailType': destination_name,
                            'Resources': self.aws_resource_arns,
                            'Source': destination_name
                        }
                    ]
                )
            ),
            timeout=self.submit_timeout
        )

    async def close(self):
        self._executor.shutdown(wait=False, cancel_futures=True)