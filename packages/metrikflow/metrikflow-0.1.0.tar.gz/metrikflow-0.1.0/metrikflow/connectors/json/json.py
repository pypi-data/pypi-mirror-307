from __future__ import annotations

import asyncio
import datetime
import functools
import json
import os
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, TextIO, Union

from metrikflow.connectors.common.signals import (
    add_signal_handler,
    handle_file_stop,
    handle_loop_stop,
)
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .json_config import JSONConfig

has_connector = True

class JSON:
    has_connector=has_connector

    def __init__(self, config: JSONConfig) -> None:

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )
        self._loop: asyncio.AbstractEventLoop = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self.metrics_file: TextIO = None

        self.write_mode = 'w' if config.overwrite else 'a'
        self.pattern = re.compile("_copy[0-9]+")
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

        metrics_data: Dict[
            str, 
            List[Dict[str, Any]]
        ] = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                json.load,
                self.metrics_file
            )
        )

        metrics: List[
            Dict[str, Any]
        ] = list(
            sorted(
                metrics_data.get(metric.name, []),
                key=lambda metric: datetime.datetime.strptime(
                    metric.get('timestamp'),
                    '%Y-%m-%dT%H:%M:%S.%f.%z'
                )
            )
        )

        if len(metrics) < 1:
            return None

        return self._store.parse(
            metrics[-1]
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

        data = metric.to_data_dict()

        add_signal_handler(
            self._loop,
            handle_file_stop,
            self.metrics_file
        )


        if file_exists:

            self.metrics_file = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    open,
                    absolute_path,
                    'r'
                )
            )
  
            metrics_data: Dict[
                str, 
                List[Dict[str, Any]]
            ] = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    json.load,
                    self.metrics_file
                )
            )

            metrics = metrics_data.get(metric.name, [])
            metrics.append(data)
            metrics_data[metric.name] = metrics

            await self._loop.run_in_executor(
                self._executor,
                self.metrics_file.close
            )

            self.metrics_file = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    open,
                    absolute_path,
                    'w'
                )
            )

            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    json.dump,
                    metrics_data,
                    self.metrics_file,
                    indent=4
                )
            )
            
        else:

            self.metrics_file = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    open,
                    absolute_path,
                    'w+'
                )
            )

            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    json.dump,
                    {
                        metric.name: [
                            data
                        ]
                    },
                    self.metrics_file,
                    indent=4
                )
            )

    async def close(self):

        if self.metrics_file:
            await self._loop.run_in_executor(
                self._executor,
                self.metrics_file.close
            )

        self._executor.shutdown(wait=False, cancel_futures=True)