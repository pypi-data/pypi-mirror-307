from datadog_api_client.v1.model.change_widget_definition import ChangeWidgetDefinition
from datadog_api_client.v1.model.change_widget_definition_type import ChangeWidgetDefinitionType
from datadog_api_client.v1.model.change_widget_request import ChangeWidgetRequest
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
from datadog_api_client.v1.model.widget_sort import WidgetSort
from datadog_api_client.v1.model.widget_formula import WidgetFormula
from datadog_api_client.v1.model.widget_order_by import WidgetOrderBy
from datadog_api_client.v1.model.widget_formula_limit import WidgetFormulaLimit
from datadog_api_client.v1.model.widget_change_type import WidgetChangeType
from datadog_api_client.v1.model.widget_compare_to import WidgetCompareTo
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
from datadog_api_client.v1.model.widget_time import WidgetTime
from metrikflow.dashboards.datadog.models import (
    WidgetOptions,
    WidgetType
)
from metrikflow.dashboards.datadog.widgets.widget_types.base.base_widget_factory import BaseWidgetFactory
from typing import List


class ChangeFactory(BaseWidgetFactory[ChangeWidgetDefinition]):
    
    def __init__(self) -> None:
        super().__init__(WidgetType.CHANGE)

    def create(
        self,
        widget_name: str,
        options: WidgetOptions
    ):
        
        queries = self.queries[widget_name]
        
        comparator = WidgetCompareTo(
            value=options.comparison_window
        )

        change_type = WidgetChangeType(
            value=options.comparison_type
        )

        sort_direction = WidgetSort(
            value=options.order
        )

        formulas: List[WidgetFormula]= []
        for query in queries:
            formulas.extend([
                WidgetFormula(
                    formula=f'{options.comparison_window}({query.to_query_name()})'
                ),
                WidgetFormula(
                    formula=query.to_query_name(),
                    limit=WidgetFormulaLimit(
                        count=options.limit,
                        order=options.to_datadog_sort_order()
                    )
                )
            ])

        change = ChangeWidgetDefinition(
            title=widget_name,
            title_size='16',
            title_align=WidgetTextAlign.LEFT,
            type=ChangeWidgetDefinitionType.CHANGE,
            time=WidgetTime(
                live_span=options.to_datadog_live_span()
            ),
            requests=[
                ChangeWidgetRequest(
                    formulas=formulas,
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
                        )   for query in queries
                    ],
                    compare_to=comparator,
                    change_type=change_type,
                    order_dir=sort_direction,
                    order_by=options.to_widget_order_by(),
                    response_format=FormulaAndFunctionResponseFormat.SCALAR,
                    show_present=options.display_current_values
                )
            ],
        )

        self._widgets[widget_name] = change

        return change

