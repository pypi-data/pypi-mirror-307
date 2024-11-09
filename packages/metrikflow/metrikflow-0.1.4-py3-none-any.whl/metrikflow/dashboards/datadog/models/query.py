import re
from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Union, Literal, Optional, Any

class Query(BaseModel):
    aggregator: Union[
        Literal['avg'],
        Literal['sum'],
        Literal['min'],
        Literal['max']
    ]='avg'
    metric: StrictStr
    aggregation_field: Optional[StrictStr]=None
    formula_type: Optional[Any]=None

    class Config:
        arbitrary_types_allowed=True

    def to_query(self):

        metric_name = self.metric.replace('-', '_')
        query_string = [
            f'{self.aggregator}:{metric_name}', 
            '{*}'
        ]
     

        if self.aggregation_field:
            query_string.extend([
                ' by {',
                self.aggregation_field,
                '}'
            ])

        return ''.join(query_string)
    
    def to_query_name(self):
        return re.sub(r"[&.-]", "_", self.metric)