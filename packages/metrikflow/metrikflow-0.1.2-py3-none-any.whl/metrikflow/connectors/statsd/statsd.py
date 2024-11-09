import uuid
from typing import Callable, Dict, Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate
from metrikflow.metrics.types.base import MetricTypes

from .statsd_config import StatsDConfig

try:
    from aio_statsd import StatsdClient
    has_connector = True

except Exception:
    StatsdClient = None
    has_connector = False


class StatsD:
    has_connector=has_connector

    def __init__(self, config: StatsDConfig) -> None:
        self.host = config.host
        self.port = config.port

        self.connection = StatsdClient(
            host=self.host,
            port=self.port
        )

        self._update_map: Dict[
            str,
            Callable[
                [
                    str,
                    Union[int, float],
                    Union[int, float],
                    Dict[str, str]
                ],
                None
            ]
        ] = {
            'count': self.connection.counter,
            'gauge': self.connection.gauge,
            'increment': self.connection.increment,
            'sets': self.connection.sets,
            'histogram': lambda: NotImplementedError('StatsD does not support histograms.'),
            'distribution': lambda: NotImplementedError('StatsD does not support distributions.'),
            'timer': self.connection.timer

        }

        self.stat_type_map = {
            MetricTypes.EVENT: 'gauge',
            MetricTypes.INTERVAL: 'gauge',
            MetricTypes.RATE: 'gauge'
        }

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self.statsd_type = 'StatsD'

    async def connect(self):
        await self.connection.connect()

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
        raise Exception('Err. - StatsD connector is send only.')

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
        metric_type = self.stat_type_map.get(
            metric.kind,
            'gauge'
        )

        metric_name = f'{metric.name}_{metric.group}'

        update_function = self._update_map.get(metric_type)
        update_function(
            metric_name,
            metric.value
        )

    async def close(self):
        await self.connection.close()
