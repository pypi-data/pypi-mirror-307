from datadog_api_client.v1.model.query_value_widget_definition import QueryValueWidgetDefinition
from datadog_api_client.v1.model.query_value_widget_definition_type import QueryValueWidgetDefinitionType
from datadog_api_client.v1.model.query_value_widget_request import QueryValueWidgetRequest
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.formula_and_function_response_format import (
    FormulaAndFunctionResponseFormat
)
from datadog_api_client.v1.model.widget_formula import WidgetFormula
from datadog_api_client.v1.model.widget_time import WidgetTime
from datadog_api_client.v1.model.widget_style import WidgetStyle
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from metrikflow.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrikflow.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory


class QueryValueFactory(BaseWidgetFactory[QueryValueWidgetDefinition]):

    def __init__(self) -> None:
        super().__init__(WidgetType.QUERY_VALUE)

        self._options = [
            'custom_unit',
            'precision'
        ]

    def create(
        self,
        widget_name: str,
        options: WidgetOptions       
    ):
        
        queries = self.queries[widget_name]

        widget_options = options.to_options(self._options)

        query_value = QueryValueWidgetDefinition(
            title=widget_name,
            title_size="16",
            title_align=WidgetTextAlign.LEFT,
            type=QueryValueWidgetDefinitionType.QUERY_VALUE,
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            autoscale=True,
            requests=[
                QueryValueWidgetRequest(
                    formulas=[
                        WidgetFormula(
                            formula=' + '.join([
                                query.to_query_name() for query in queries
                            ])
                        )
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
                    response_format=FormulaAndFunctionResponseFormat.SCALAR,
                )
            ],
            **widget_options
        )

        self._widgets[widget_name] = query_value

        return query_value