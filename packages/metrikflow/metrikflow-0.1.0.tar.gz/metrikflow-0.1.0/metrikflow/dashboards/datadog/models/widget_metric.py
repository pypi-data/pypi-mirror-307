from pydantic import (
    BaseModel,
    StrictStr
)
from metrik.metrics.types import (
    Event,
    Interval,
    Rate
)
from .widget_options import WidgetOptions
from typing import (
    Optional, 
    Union,
    Literal
)


class WidgetMetric(BaseModel):
    widget_name: StrictStr
    widget_type: Literal[
        'change',
        'histogram',
        'query_value',
        'scatter_plot',
        'table',
        'timeseries'
    ]='timeseries'
    metric: Union[
        Event,
        Interval,
        Rate
    ]
    widget_size: Union[
        Literal['extra_small'],
        Literal['small'],
        Literal['medium'],
        Literal['large'],
        Literal['extra_large']
    ]='medium'
    widget_aggregator: Union[
        Literal['average'],
        Literal['total'],
        Literal['maximum'],
        Literal['minimum']
    ]='average'
    widget_aggregator_field: Optional[StrictStr]=None
    widget_options: Optional[WidgetOptions]=None
