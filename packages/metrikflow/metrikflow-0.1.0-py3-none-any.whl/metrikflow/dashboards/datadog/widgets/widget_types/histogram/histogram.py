from datadog_api_client.v1.model.distribution_widget_definition import DistributionWidgetDefinition
from datadog_api_client.v1.model.distribution_widget_definition_type import DistributionWidgetDefinitionType
from datadog_api_client.v1.model.distribution_widget_histogram_request_type import (
    DistributionWidgetHistogramRequestType,
)
from datadog_api_client.v1.model.distribution_widget_request import DistributionWidgetRequest
from datadog_api_client.v1.model.distribution_widget_x_axis import DistributionWidgetXAxis
from datadog_api_client.v1.model.distribution_widget_y_axis import DistributionWidgetYAxis
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.widget_time import WidgetTime
from datadog_api_client.v1.model.widget_style import WidgetStyle
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from metrik.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrik.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory


class HistogramFactory(BaseWidgetFactory[DistributionWidgetDefinition]):
    
    def __init__(self) -> None:
        super().__init__(WidgetType.HISTOGRAM)

    def create(
        self,
        widget_name: str,
        options: WidgetOptions
    ):
        
        queries = self.queries[widget_name]
        
        histogram = DistributionWidgetDefinition(
            title=widget_name,
            title_size="16",
            title_align=WidgetTextAlign.LEFT,
            show_legend=True,
            type=DistributionWidgetDefinitionType.DISTRIBUTION,
            legend_size='12',
            xaxis=DistributionWidgetXAxis(
                max="auto",
                include_zero=True,
                scale="linear",
                min="auto",
            ),
            yaxis=DistributionWidgetYAxis(
                max="auto",
                include_zero=True,
                scale="linear",
                min="auto",
            ),
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            requests=[
                DistributionWidgetRequest(
                    query=FormulaAndFunctionMetricQueryDefinition(
                        data_source=FormulaAndFunctionMetricDataSource.METRICS,
                        name=query.to_query_name(),
                        aggregator=query.formula_type,
                        query=query.to_query()
                    ) if query.aggregation_field else FormulaAndFunctionMetricQueryDefinition(
                        data_source=FormulaAndFunctionMetricDataSource.METRICS,
                        name=query.to_query_name(),
                        query=query.to_query()
                    ),
                    style=WidgetStyle(
                        palette="dog_classic",
                    ),
                )  for query in queries
            ],
        )

        self._widgets[widget_name] = histogram

        return histogram