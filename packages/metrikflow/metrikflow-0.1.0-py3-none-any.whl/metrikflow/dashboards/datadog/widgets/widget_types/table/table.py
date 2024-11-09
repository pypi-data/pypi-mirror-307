from datadog_api_client.v1.model.table_widget_definition import TableWidgetDefinition
from datadog_api_client.v1.model.table_widget_definition_type import TableWidgetDefinitionType
from datadog_api_client.v1.model.table_widget_cell_display_mode import TableWidgetCellDisplayMode
from datadog_api_client.v1.model.table_widget_has_search_bar import TableWidgetHasSearchBar
from datadog_api_client.v1.model.table_widget_request import TableWidgetRequest
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from datadog_api_client.v1.model.widget_formula import WidgetFormula
from datadog_api_client.v1.model.widget_formula_limit import WidgetFormulaLimit
from datadog_api_client.v1.model.widget_style import WidgetStyle
from datadog_api_client.v1.model.widget_time import WidgetTime
from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
    FormulaAndFunctionMetricQueryDefinition,
)
from datadog_api_client.v1.model.formula_and_function_metric_data_source import (
    FormulaAndFunctionMetricDataSource,
)
from datadog_api_client.v1.model.formula_and_function_response_format import (
    FormulaAndFunctionResponseFormat
)
from metrik.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrik.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory


class TableFactory(BaseWidgetFactory[TableWidgetDefinition]):

    def __init__(self) -> None:
        super().__init__(WidgetType.TABLE)

    def create(
        self,
        widget_name: str,
        options: WidgetOptions
    ):
        
        queries = self.queries[widget_name]
        
        table = TableWidgetDefinition(
            title=widget_name,
            title_size='16',
            title_align=WidgetTextAlign.LEFT,
            type=TableWidgetDefinitionType.QUERY_TABLE,
            has_search_bar=options.to_search_bar_type(),
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            requests=[
                TableWidgetRequest(
                    formulas=[
                        WidgetFormula(
                            formula=' + '.join([
                                query.to_query_name() for query in queries
                            ]),
                            limit=WidgetFormulaLimit(
                                count=options.limit,
                                order=options.to_datadog_sort_order()
                            ),
                            cell_display_mode=options.to_datadog_cell_display_mode()
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
                        ) for query in queries
                    ],
                    response_format=FormulaAndFunctionResponseFormat.SCALAR
                )
            ]
        )

        self._widgets[widget_name] = table

        return table