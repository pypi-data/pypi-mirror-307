import uuid
from typing import Callable, Dict, Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate
from metrikflow.metrics.types.base import MetricTypes

from .dogstatsd_config import DogStatsDConfig

try:
    from aio_statsd import DogStatsdClient

    from metrikflow.connectors.statsd import StatsD
    has_connector = True

except Exception:
    from metrikflow.connectors.empty import Empty as StatsD
    DogStatsdClient = None
    has_connector = False


class DogStatsD(StatsD):
    has_connector=has_connector

    def __init__(self, config: DogStatsDConfig) -> None:
        super(DogStatsD, self).__init__(config)
    
        self.host = config.host
        self.port = config.port

        self.connection = DogStatsdClient(
            host=self.host,
            port=self.port
        )

        self.stat_type_map = {
            MetricTypes.EVENT: 'gauge',
            MetricTypes.INTERVAL: 'gauge',
            MetricTypes.RATE: 'gauge'
        }

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
            'count': lambda: NotImplementedError('DogStatsD does not support counts.'),
            'gauge': self.connection.gauge,
            'sets': lambda: NotImplementedError('DogStatsD does not support sets.'),
            'increment': self.connection.increment,
            'histogram': self.connection.histogram,
            'distribution': self.connection.distribution,
            'timer': self.connection.timer
        }

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self.statsd_type = 'StatsD'

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
        raise Exception('Err. - DogStatsD connector is send only.')
        

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

        metric_key = f'{destination_name}_{metric.name}'

        update_function = self._update_map.get(metric_type)
        update_function(
            metric_key,
            metric.value,
            sample_rate=1 if metric.kind == MetricTypes.RATE else None,
            tag_dict=metric.to_tags_dict()
        )

    async def close(self):
        await self.connection.close()