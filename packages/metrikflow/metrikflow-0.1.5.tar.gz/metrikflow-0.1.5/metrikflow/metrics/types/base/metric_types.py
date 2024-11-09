from enum import Enum
from typing import TypedDict, Literal, Union


class MetricTypes(Enum):
    EVENT='EVENT'
    INTERVAL='INTERVAL'
    RATE='RATE'



class MetricTypesDict(TypedDict):
    event: Literal[MetricTypes.EVENT]
    interval: Literal[MetricTypes.INTERVAL]
    rate: Literal[MetricTypes.RATE]


class MetricTypesMap:

    def __init__(self) -> None:
        super().__init__()

        self._types: MetricTypesDict = {
            'event': MetricTypes.EVENT,
            'interval': MetricTypes.INTERVAL,
            'rate': MetricTypes.RATE
        }

    def __getitem__(
        self, 
        metric_type: Union[
            Literal['event'],
            Literal['interval'],
            Literal['rate']
        ]
    ):
        return self._types[metric_type]
    
    def get(
        self,
        metric_type: Union[
            Literal['event'],
            Literal['interval'],
            Literal['rate']
        ]
    ):
        if metric_type in self._types:
            return self._types[metric_type]
        
        return MetricTypes.EVENT
