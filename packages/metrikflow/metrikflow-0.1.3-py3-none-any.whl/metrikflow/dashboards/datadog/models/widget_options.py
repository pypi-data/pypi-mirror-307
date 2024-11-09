from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    validator
)
from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
from datadog_api_client.v1.model.widget_live_span import WidgetLiveSpan
from datadog_api_client.v1.model.query_sort_order import QuerySortOrder
from datadog_api_client.v1.model.widget_order_by import WidgetOrderBy
from datadog_api_client.v1.model.table_widget_has_search_bar import TableWidgetHasSearchBar
from typing import (
    Literal,
    Union,
    Optional,
    List,
    Dict
)


class WidgetOptions(BaseModel):
    cell_display_mode: Union[
        Literal['bar'],
        Literal['number']
    ]='number'
    comparison_window: Union[
        Literal['day_before'],
        Literal['hour_before'],
        Literal['month_before'],
        Literal['week_before']
    ]='hour_before'
    comparison_type: Union[
        Literal['absolute'],
        Literal['relative']
    ]='absolute'
    limit: StrictInt=10
    order: Union[
        Literal['asc'],
        Literal['desc']
    ]='desc'
    order_by: Literal[
        'change',
        'name',
        'past',
        'present'
    ]='change',
    show_increase_as_positive: StrictBool=True
    custom_unit: Optional[StrictStr]=None
    precision: StrictInt=2
    search_bar_type: Literal[
        'always',
        'never',
        'auto'
    ]='auto'
    window: Literal[
        '1m',
        '5m',
        '10m',
        '15m',
        '30m',
        '1h',
        '4h',
        '1d',
        '2d',
        '1w',
        '1mo',
        '3mo',
        '6mo',
        '1y',
        'alert'
    ]='1d'
    x_axis_name: Optional[StrictStr]=None
    y_axis_name: Optional[StrictStr]=None
    x_axis_metrics: List[StrictStr]=[]
    y_axis_metrics: List[StrictStr]=[]
    display_current_values: StrictBool=True

    @validator('x_axis_name')
    def validate_x_axis_metrics(cls, v):

        if cls.x_axis_name is not None:
            assert len(cls.x_axis_metrics) > 0, "At least one metric must be specified as part of the X axis if an X axis is specified"

    @validator('y_axis_name')
    def validate_y_axis_metrics(cls, v):

        if cls.y_axis_name is not None:
            assert len(cls.y_axis_metrics) > 0, "At least one metric must be specified as part of the Y axis if an Y axis is specified"

    def to_datadog_sort_order(self):
        return QuerySortOrder.ASC if self.order == 'asc' else QuerySortOrder.DESC
    
    def to_datadog_live_span(self):

        live_spans: Dict[
            Literal[
                '1m',
                '5m',
                '10m',
                '15m',
                '30m',
                '1h',
                '4h',
                '1d',
                '2d',
                '1w',
                '1mo',
                '3mo',
                '6mo',
                '1y',
                'week_to_date',
                'month_to_date',
                'alert'
            ]
        ] = {
            '1m': WidgetLiveSpan.PAST_ONE_MINUTE,
            '5m': WidgetLiveSpan.PAST_FIVE_MINUTES,
            '10m': WidgetLiveSpan.PAST_TEN_MINUTES,
            '15m': WidgetLiveSpan.PAST_FIFTEEN_MINUTES,
            '30m': WidgetLiveSpan.PAST_THIRTY_MINUTES,
            '1h': WidgetLiveSpan.PAST_ONE_HOUR,
            '4h': WidgetLiveSpan.PAST_FOUR_HOURS,
            '1d': WidgetLiveSpan.PAST_ONE_DAY,
            '2d': WidgetLiveSpan.PAST_TWO_DAYS,
            '1w': WidgetLiveSpan.PAST_ONE_WEEK,
            '1mo': WidgetLiveSpan.PAST_ONE_MONTH,
            '3mo': WidgetLiveSpan.PAST_THREE_MONTHS,
            '6mo': WidgetLiveSpan.PAST_SIX_MONTHS,
            '1y': WidgetLiveSpan.PAST_ONE_YEAR,
            'alert': WidgetLiveSpan.ALERT

        }

        return live_spans.get(
            self.window,
            WidgetLiveSpan.PAST_ONE_DAY
        )
    
    def to_datadog_cell_display_mode(self):
        return TableWidgetCellDisplayMode.BAR if self.cell_display_mode == 'bar' else TableWidgetCellDisplayMode.NUMBER
    
    def to_widget_order_by(self):
        order_types: Dict[
            str,
            WidgetOrderBy
        ] = {
            'change': WidgetOrderBy.CHANGE,
            'name': WidgetOrderBy.NAME,
            'past': WidgetOrderBy.PAST,
            'present': WidgetOrderBy.PRESENT
        }

        return order_types.get(
            self.order_by,
            WidgetOrderBy.CHANGE
        )
    
    def to_search_bar_type(self):
        search_bar_types: Dict[
            str,
            TableWidgetHasSearchBar
        ] = {
            'always': TableWidgetHasSearchBar.ALWAYS,
            'never': TableWidgetHasSearchBar.NEVER,
            'auto': TableWidgetHasSearchBar.AUTO
        }

        return search_bar_types.get(
            self.search_bar_type,
            TableWidgetHasSearchBar.AUTO
        )
    
    def to_options(
        self,
        widget_supported_options: List[str]
    ):
        return {
            option_name: option_value for option_name, option_value in self.dict().items() if option_name in widget_supported_options and option_value is not None
        }