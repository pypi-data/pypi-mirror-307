import datetime
import json
from collections import defaultdict
from .types.base import UnitTypesMap
from .types import (
    Event,
    Interval,
    Rate
)
from typing import (
    Union, 
    Dict, 
    List,
    Literal,
    Callable,
    Any,
    Optional
)


class MetricStore:

    def __init__(self) -> None:
        self._registered: Dict[
            str,
            Dict[
                str,
                Union[
                    Event,
                    Interval,
                    Rate
                ]
            ]
        ] = defaultdict(dict)

        self._types: Dict[
            Union[
                Literal['event'],
                Literal['interval'],
                Literal['rate']
            ],
            Union[
                Callable[..., Event],
                Callable[..., Interval],
                Callable[..., Rate]
            ]
        ] = {
            'event': lambda kwargs: Event.parse(kwargs),
            'interval': lambda kwargs: Interval.parse(kwargs),
            'rate': lambda kwargs: Rate.parse(kwargs)
        }

        self._units_map = UnitTypesMap()

    def create_load_query(
        self,
        name: str=None,
        kind: Union[
            Literal['event'],
            Literal['interval'],
            Literal['rate']
        ]=None,
        group: str=None,
        timestamp: datetime.datetime=None,
        value: Union[
            int,
            float,
            datetime.datetime,
            str
        ]=None
    ):
        return self._types[kind]({
            'name': name,
            'group': group,
            'timestamp': timestamp,
            'value': value
        })

    def parse(
        self,
        metric_data: Union[
            str,
            bytes,
            Dict[str, Any]
        ]
    ):
        
        if isinstance(metric_data, (str, bytes)):
            metric_data: Dict[str, Any] = json.loads(metric_data)

        timestamp = metric_data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.datetime.strptime(
                timestamp,
                '%Y-%m-%dT%H:%M:%S.%f.%z'
            )

            metric_data['timestamp'] = timestamp

        elif isinstance(timestamp, bytes):
            timestamp = datetime.datetime.strptime(
                timestamp.decode(),
                '%Y-%m-%dT%H:%M:%S.%f.%z'
            )

            metric_data['timestamp'] = timestamp

        metric_data['unit'] = self._types.get(
            metric_data.get('unit')
        )
        
        kind: Union[str, bytes] = metric_data.get('kind')
        if kind:
            kind = kind.lower()

        if kind not in self._types:
            raise Exception(f'Err. - Invalid metric kind - {kind} - cannot parse.')

        return self._types[kind](metric_data)

    def record(
        self,
        name: str=None,
        kind: Literal[
            'event',
            'interval',
            'rate'
        ]=None,
        group: str=None,
        timestamp: datetime.datetime=None,
        value: Union[
            int,
            float,
            datetime.datetime,
            str
        ]=None,
        tags: Optional[
            List[
                Dict[str, str]
            ]
        ]=None,
        unit: Literal[
            'nanoseconds',
            'microseconds',
            'milliseconds',
            'seconds',
            'minutes',
            'hours',
            'days',
            'weeks'
        ]=None
    ):
        
        if group is None:
            group = 'default'
        
        metric = self._registered[group].get(name)
        if metric is None:
            metric = self._types[kind]({
                'name': name,
                'group': group,
                'timestamp': timestamp,
                'value': value,
                'tags': tags,
                'unit': self._units_map.get(unit)
            })

            self._registered[group][name] = metric

        else:

            self._registered[group][name].update(
                value,
                tags=tags
            )

        return metric
