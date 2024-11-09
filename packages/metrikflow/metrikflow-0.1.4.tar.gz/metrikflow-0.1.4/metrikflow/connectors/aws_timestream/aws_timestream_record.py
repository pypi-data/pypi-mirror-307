
import time
from typing import Union, Any
from datetime import datetime
from metrikflow.metrics.types import (
    Event,
    Interval,
    Rate
)


class AWSTimestreamRecord:

    def __init__(
        self, 
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        session_id: str
    ) -> None:

        measure_value_type = None
        value = metric.serialize_value()

        if isinstance(value, float):
            measure_value_type = "DOUBLE"

        elif isinstance(value, str):
            measure_value_type = "VARCHAR"
        
        elif isinstance(value, bool):
            measure_value_type = "BOOLEAN"

        elif isinstance(value, int):
            measure_value_type = "BIGINT"

        elif isinstance(value, datetime):
            value = int(value.timestamp())
            measure_value_type = "TIMESTAMP"

        self.record_kind = metric.kind.value
        self.record_name = metric.name
        self.field = 'value'

        self.time = str(int(round(time.time() * 1000)))
        self.time_unit = 'MILLISECONDS'
        self.dimensions = [
            {
                "Name": "metric_id",
                "Value": metric.metric_id
            },
            {
                "Name": "name",
                "Value": metric.name
            },
            {
                "Name": "kind",
                "Value": metric.kind.value
            },
            {
                "Name": "timestamp",
                "Value": metric.to_date_string()
            },
            {
                "Name": "session_id",
                "Value": session_id
            }
        ]
        self.measure_name = f'{metric.name}_{metric.group}_{session_id}'
        self.measure_value = str(value)
        self.measure_value_type = measure_value_type

    def to_dict(self):
        return  {
            "Time": self.time,
            "TimeUnit": self.time_unit,
            "Dimensions": self.dimensions,
            "MeasureName": self.measure_name,
            "MeasureValue": self.measure_value,
            "MeasureValueType": self.measure_value_type
        }
    
    @classmethod
    def parse_type(
        cls,
        column_type: str,
        value: str
    ):
        match column_type:
            case 'VARCHAR':
                return value
            
            case 'BOOLEAN':
                return True if value.lower() == 'true' else False

            case 'BIGINT' | 'INTEGER' | 'TIME':
                return int(value)
            
            case 'DOUBLE':
                return float(value)
            
            case 'DATE':
                return datetime.strptime(
                    value,
                    '%Y-%m-%d'
                )
            
            case 'TIMESTAMP':
                return datetime.strptime(
                    value,
                    '%Y-%m-%dT%H:%M:%S.%f.%z'
                )
            
            case _:
                return value
