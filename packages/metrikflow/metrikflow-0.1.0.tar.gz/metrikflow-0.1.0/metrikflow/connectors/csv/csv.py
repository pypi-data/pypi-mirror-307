import asyncio
import csv
import datetime
import functools
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, TextIO, Union

from metrikflow.connectors.common.signals import (
    add_signal_handler,
    handle_file_stop,
    handle_loop_stop,
)
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .csv_config import CSVConfig

has_connector = True


class CSV:
    has_connector=has_connector

    def __init__(self, config: CSVConfig) -> None:
        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._csv_reader: Union[csv.DictReader, None] = None
        self._csv_writer: Union[csv.DictWriter, None] = None

        self._loop: asyncio.AbstractEventLoop = None

        self.metrics_file: TextIO = None 

        self.write_mode = 'w' if config.overwrite else 'a'
        self._store = MetricStore()

    async def connect(self):
        self._loop = asyncio._get_running_loop()

        add_signal_handler(
            self._loop,
            handle_loop_stop,
            self._executor,
            self._loop
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
        absolute_path = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                os.path.abspath,
                source_name
            )
        )

        file_exists = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                os.path.exists,
                absolute_path
            )
        )

        if file_exists is False:
            return None

        self.metrics_file = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                open,
                absolute_path,
                'r'
            )
        )

        add_signal_handler(
            self._loop,
            handle_file_stop,
            self.metrics_file
        )

        lines = await self._loop.run_in_executor(
            self._executor,
            self.metrics_file.readlines
        )

        self._csv_reader = csv.DictReader(
            lines, 
            metric.to_column_names()
        )

        metric_records: List[
            Dict[str, any]
        ] = list(
            sorted(
                [
                    line for line in self._csv_reader if line.get(
                        'name'
                    ) == metric.name
                ],
                key=lambda record: datetime.datetime.strptime(
                    record.get('timestamp'),
                    '%Y-%m-%dT%H:%M:%S.%f.%z'
                )
            )
        )

        if len(metric_records) < 1:
            return None

        return self._store.parse(
            metric_records[-1]
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
        
        absolute_path = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                os.path.abspath,
                destination_name
            )
        )


        file_exists = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                os.path.exists,
                absolute_path
            )
        )
        
        self.metrics_file = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                open,
                absolute_path,
                'a+'
            )
        )

        add_signal_handler(
            self._loop,
            handle_file_stop,
            self.metrics_file
        )

        self._csv_writer = csv.DictWriter(
            self.metrics_file,
            metric.to_column_names()
        )


        if file_exists is False:
            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self._csv_writer.writeheader
                )
            )

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._csv_writer.writerow,
                metric.dict()
            )
        )

    async def close(self):
        await self._loop.run_in_executor(
            self._executor,
            self.metrics_file.close
        )

        self._executor.shutdown(wait=False, cancel_futures=True)