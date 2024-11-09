import asyncio
import collections
import collections.abc
import datetime
import functools
import os
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

from .xml_config import XMLConfig

try:
    from dicttoxml import dicttoxml
    from xmltodict import parse
    has_connector=True

except Exception:
    dicttoxml = object
    has_connector=False

collections.Iterable = collections.abc.Iterable


MetricRecord = Dict[str, Union[int, float, str]]
MetricRecordGroup = Dict[str, List[MetricRecord]]
MetricRecordCollection = Dict[str, MetricRecord]
    

class XML:
    has_connector=has_connector
    
    def __init__(self, config: XMLConfig) -> None:

        self._executor = ThreadPoolExecutor(
            os.cpu_count()
        )
        self._loop: asyncio.AbstractEventLoop = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self.metrics_file: TextIO = None
        self._store = MetricStore()

        self.write_mode = 'w' if config.overwrite else 'a'

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

        data = await self._loop.run_in_executor(
            self._executor,
            self.metrics_file.read
        )

        metrics_data = parse(data)

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

        self.metrics_file = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                open,
                absolute_path,
                'r+'
            )
        )

        add_signal_handler(
            self._loop,
            handle_file_stop,
            self.metrics_file
        )

        if file_exists:
            
            data: str = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.metrics_file.read
                )
            )

            metrics_data: Dict[
                str, 
                List[Dict[str, Any]]
            ] = parse(data)

            metrics = metrics_data.get(metric.name, [])
            metrics.append(data)
            metrics_data[metric.name] = metrics

            xml_data = dicttoxml(metrics_data)

            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.metrics_file.write,
                    xml_data
                )
            )

        else:
            xml_data = dicttoxml({
                metric.name: [
                    metric.to_data_dict()
                ]
            })

            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.metrics_file.write,
                    xml_data
                )
            )

    async def close(self):

        await self._loop.run_in_executor(
            self._executor,
            self.metrics_file.close
        )

        self._executor.shutdown(wait=False, cancel_futures=True)