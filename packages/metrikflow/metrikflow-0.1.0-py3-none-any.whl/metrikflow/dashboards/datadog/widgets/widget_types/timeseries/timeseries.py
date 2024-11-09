from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import (
    TimeseriesWidgetRequest,
)
from datadog_api_client.v1.model.timeseries_widget_legend_column import TimeseriesWidgetLegendColumn
from datadog_api_client.v1.model.timeseries_widget_legend_layout import TimeseriesWidgetLegendLayout
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.formula_and_function_response_format import (
    FormulaAndFunctionResponseFormat
)
from datadog_api_client.v1.model.widget_formula_style import WidgetFormulaStyle
from datadog_api_client.v1.model.widget_time import WidgetTime
from datadog_api_client.v1.model.widget_formula import WidgetFormula
from metrik.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrik.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory


class TimeseriesFactory(BaseWidgetFactory[TimeseriesWidgetDefinition]):

    def __init__(self) -> None:
        super().__init__(WidgetType.TIMESERIES)
    
    def create(
        self,
        widget_name: str,
        options: WidgetOptions
    ):
        
        queries = self.queries[widget_name]


        timeseries = TimeseriesWidgetDefinition(
            title=widget_name,
            title_size="16",
            title_align=WidgetTextAlign.LEFT,
            show_legend=True,
            type=TimeseriesWidgetDefinitionType.TIMESERIES,
            legend_columns=[
                TimeseriesWidgetLegendColumn.AVG,
                TimeseriesWidgetLegendColumn.SUM,
                TimeseriesWidgetLegendColumn.MAX,
                TimeseriesWidgetLegendColumn.MIN,
                TimeseriesWidgetLegendColumn.VALUE
            ],
            legend_layout=TimeseriesWidgetLegendLayout.AUTO,
            legend_size='12',
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            requests=[
                TimeseriesWidgetRequest(
                    formulas=[
                        WidgetFormula(
                            formula=query.to_query_name()
                        ) for query in queries
                    ],
                    queries=[
                        FormulaAndFunctionMetricQueryDefinition(
                            data_source=FormulaAndFunctionMetricDataSource.METRICS,
                            name=query.to_query_name(),
                            query=query.to_query()
                        )  for query in queries
                    ],
                    response_format=FormulaAndFunctionResponseFormat.TIMESERIES
                )
            ]
        )

        self._widgets[widget_name] = timeseries

        return timeseries