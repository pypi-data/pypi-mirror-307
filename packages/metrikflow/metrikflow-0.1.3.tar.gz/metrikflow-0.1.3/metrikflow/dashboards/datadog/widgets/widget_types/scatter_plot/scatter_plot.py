from datadog_api_client.v1.model.scatter_plot_widget_definition import ScatterPlotWidgetDefinition
from datadog_api_client.v1.model.scatter_plot_widget_definition_type import ScatterPlotWidgetDefinitionType
from datadog_api_client.v1.model.scatter_plot_widget_definition_requests import ScatterPlotWidgetDefinitionRequests
from datadog_api_client.v1.model.scatterplot_table_request import ScatterplotTableRequest
from datadog_api_client.v1.model.scatterplot_widget_formula import ScatterplotWidgetFormula
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.formula_and_function_response_format import (
    FormulaAndFunctionResponseFormat
)
from datadog_api_client.v1.model.widget_axis import WidgetAxis
from datadog_api_client.v1.model.widget_style import WidgetStyle
from datadog_api_client.v1.model.widget_time import WidgetTime
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from metrikflow.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrikflow.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory


class ScatterPlotFactory(BaseWidgetFactory[ScatterPlotWidgetDefinition]):

    def __init__(self) -> None:
        super().__init__(WidgetType.SCATTER_PLOT)

    def create(
        self,
        widget_name: str,
        options: WidgetOptions
    ):   
        queries = self.queries[widget_name]
  
        scatter_plot = ScatterPlotWidgetDefinition(
            title=widget_name,
            title_size='16',
            title_align=WidgetTextAlign.LEFT,
            type=ScatterPlotWidgetDefinitionType.SCATTERPLOT,
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            xaxis=WidgetAxis(
                label=options.x_axis_name,
                max="auto",
                include_zero=True,
                scale="linear",
                min="auto",
            ),
            yaxis=WidgetAxis(
                label=options.y_axis_name,
                max="auto",
                include_zero=True,
                scale="linear",
                min="auto",
            ),
            requests=[
                ScatterPlotWidgetDefinitionRequests(
                    table=ScatterplotTableRequest(
                        formulas=[
                            ScatterplotWidgetFormula(
                                formula=query.to_query_name(),
                                dimension='x' if query.metric in options.x_axis_metrics else 'y',
                            ) for  query in queries
                        ],
                        queries=[
                            FormulaAndFunctionMetricQueryDefinition(
                            data_source=FormulaAndFunctionMetricDataSource.METRICS,
                            name=query.to_query_name(),
                            aggregator=query.formula_type,
                            query=query.to_query()
                        ) if query.aggregation_field else FormulaAndFunctionMetricQueryDefinition(
                            data_source=FormulaAndFunctionMetricDataSource.METRICS,
                            name=query.to_query_name(),
                            query=query.to_query()
                        )  for query in queries
                        ],
                        response_format=FormulaAndFunctionResponseFormat.TIMESERIES
                    )
                )
            ]
        )

        self._widgets[widget_name] = scatter_plot

        return scatter_plot