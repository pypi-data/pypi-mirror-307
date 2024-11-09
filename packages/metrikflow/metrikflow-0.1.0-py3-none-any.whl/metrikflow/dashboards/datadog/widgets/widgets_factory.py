from collections import OrderedDict
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.widget import Widget
from metrik.dashboards.datadog.layouts import (
    Layout,
    SizeTypeMap
)
from metrik.dashboards.datadog.models import (
    WidgetMetric,
    Query,
    WidgetAggregationTypeMap,
    WidgetOptions,
    WidgetType,
    WidgetTypeMap
)
from .widget_types.change import ChangeFactory
from .widget_types.histogram import HistogramFactory
from .widget_types.query_value import QueryValueFactory
from .widget_types.scatter_plot import ScatterPlotFactory
from .widget_types.table import TableFactory
from .widget_types.timeseries import TimeseriesFactory
from typing import (
    List, 
    Dict,
    Optional,
    Union
)


class WidgetsFactory:

    def __init__(self) -> None:
        self._widgets: Dict[str, WidgetType] = OrderedDict()
        self._queries: Dict[str, FormulaAndFunctionMetricQueryDefinition]
        self._layouts = Layout()
        self._size_type_map = SizeTypeMap()
        self._widget_type_map = WidgetTypeMap()

        self._factories: Dict[
            WidgetType,
            Union[
                ChangeFactory,
                HistogramFactory,
                QueryValueFactory,
                ScatterPlotFactory,
                TableFactory,
                TimeseriesFactory,
            ]
        ] = {
            WidgetType.CHANGE: ChangeFactory(),
            WidgetType.HISTOGRAM: HistogramFactory(),
            WidgetType.QUERY_VALUE: QueryValueFactory(),
            WidgetType.SCATTER_PLOT: ScatterPlotFactory(),
            WidgetType.TABLE: TableFactory(),
            WidgetType.TIMESERIES: TimeseriesFactory()
        }

        self._aggregation_type_map = WidgetAggregationTypeMap()
        self._options: Dict[str, WidgetOptions] = {}

    def add_metric(
        self,
        widget_metric: WidgetMetric
    ):

        widget = self._widgets.get(widget_metric.widget_name)
        widget_type = self._widget_type_map[widget_metric.widget_type]
        
        if widget is None:

            self._widgets[widget_metric.widget_name] = widget_type
            widget_size = self._size_type_map[widget_metric.widget_size]

            self._options[widget_metric.widget_name] = widget_metric.widget_options

            self._layouts.add_widget(
                widget_metric.widget_name,
                widget_size
            )

            self._factories[widget_type].create_widget(
                widget_type,
                widget_size
            )

        metric_name = f'{widget_metric.metric.group}.{widget_metric.metric.name}'

        self._factories[widget_type].add_metric(
            widget_metric.widget_name,
            Query(
                aggregator=self._aggregation_type_map.map_to_datadog_type(
                    widget_metric.widget_aggregator
                ),
                metric=metric_name,
                aggregation_field=widget_metric.widget_aggregator_field,
                formula_type=self._aggregation_type_map.map_to_formula_type(
                    widget_metric.widget_aggregator
                )
            )
        )

    def to_widgets(
        self,
        options: Optional[WidgetOptions]=None
    ):
        
        widgets: List[Widget] = []
        default_options = WidgetOptions()

        for widget_name, widget_type in self._widgets.items():

            widget_options = self._options.get(widget_name)

            if widget_options is None and options is None:
                widget_options = default_options
      
            elif widget_options is None and options:
                widget_options = options

            elif widget_options and options:
                options_dict = options.dict(
                    exclude_defaults=True,
                    exclude_unset=True,
                    exclude_none=True
                )
                
                widget_options_dict = widget_options.dict(
                    exclude_defaults=True,
                    exclude_unset=True,
                    exclude_none=True
                )

                widget_options_dict.update(options_dict)

                widget_options = WidgetOptions(**widget_options_dict)
            
            widget = self._factories[widget_type].create(
                widget_name,
                widget_options
            )

            widgets.append(
                Widget(
                    definition=widget,
                    layout=self._layouts[widget_name]
                ),
            )

        return widgets
        



        
        

        

