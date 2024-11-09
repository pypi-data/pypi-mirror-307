from typing import Dict, Literal, Union
from .widget_type import WidgetType


class WidgetTypeMap:

    def __init__(self) -> None:
        self._types: Dict[
            Literal[
                'change',
                'histogram',
                'query_value',
                'scatter_plot',
                'table',
                'timeseries'
            ],
            WidgetType
        ] = {
            'change': WidgetType.CHANGE,
            'histogram': WidgetType.HISTOGRAM,
            'query_value': WidgetType.QUERY_VALUE,
            'scatter_plot': WidgetType.SCATTER_PLOT,
            'table': WidgetType.TABLE,
            'timeseries': WidgetType.TIMESERIES
        }

    def __iter__(self):
        for widget_type in self._types.values():
            yield widget_type

    def __getitem__(
        self,
        widget_type: Literal['timeseries']
    ):
        return self._types.get(
            widget_type,
            WidgetType.TIMESERIES
        )
    
    def get(
        self,
        widget_type: Literal[
            'change',
            'histogram',
            'query_value',
            'scatter_plot',
            'table',
            'timeseries'
        ]
    ):
        return self._types.get(widget_type)