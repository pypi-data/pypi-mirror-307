from datadog_api_client.v1.model.formula_and_function_metric_aggregation import (
    FormulaAndFunctionMetricAggregation
)
from typing import Dict, Literal, Union
from .widget_aggregation_type import WidgetAggregationType


class WidgetAggregationTypeMap:

    def __init__(self) -> None:
        self._types: Dict[
            Union[
                Literal['average'],
                Literal['total'],
                Literal['maximum'],
                Literal['minimum']
            ],
            Union[
                WidgetAggregationType.AVERAGE,
                WidgetAggregationType.TOTAL,
                WidgetAggregationType.MAXIMUM,
                WidgetAggregationType.MINIMUM
            ]
        ] = {
            'average': WidgetAggregationType.AVERAGE,
            'total': WidgetAggregationType.TOTAL,
            'maximum': WidgetAggregationType.MAXIMUM,
            'minimum': WidgetAggregationType.MINIMUM
        }

        self._datadog_types: Dict[
            Union[
                Literal['average'],
                Literal['total'],
                Literal['maximum'],
                Literal['minimum']
            ],
            Union[
                Literal['avg'],
                Literal['sum'],
                Literal['max'],
                Literal['min']
            ]
        ] = {
            'average': 'avg',
            'total': 'sum',
            'maximum': 'max',
            'minimum': 'min'
        }

        self._formula_types: Dict[
            Union[
                Literal['average'],
                Literal['total'],
                Literal['maximum'],
                Literal['minimum']
            ],
            Union[
                FormulaAndFunctionMetricAggregation.AVG,
                FormulaAndFunctionMetricAggregation.SUM,
                FormulaAndFunctionMetricAggregation.MAX,
                FormulaAndFunctionMetricAggregation.MIN
            ]
        ] = {
            'average': FormulaAndFunctionMetricAggregation.AVG,
            'total': FormulaAndFunctionMetricAggregation.SUM,
            'maximum': FormulaAndFunctionMetricAggregation.MAX,
            'minimum': FormulaAndFunctionMetricAggregation.MIN
        }

    def __iter__(self):
        for aggregation_type in self._types.values():
            yield aggregation_type

    def __getitem__(
        self,
        aggregation_type: Union[
            Literal['average'],
            Literal['total'],
            Literal['maximum'],
            Literal['minimum']
        ]
    ):
        return self._types.get(
            aggregation_type,
            WidgetAggregationType.AVERAGE
        )
    
    def get(
        self,
        aggregation_type: Union[
            Literal['average'],
            Literal['total'],
            Literal['maximum'],
            Literal['minimum']
        ]
    ):
        return self._types.get(aggregation_type)
    
    def map_to_datadog_type(
        self,
        aggregation_type: Union[
            Literal['average'],
            Literal['total'],
            Literal['maximum'],
            Literal['minimum']
        ]
    ):
        return self._datadog_types.get(aggregation_type)
    
    def map_to_formula_type(
        self,
        aggregation_type: Union[
            Literal['average'],
            Literal['total'],
            Literal['maximum'],
            Literal['minimum']
        ]         
    ):
        return self._formula_types.get(aggregation_type)
