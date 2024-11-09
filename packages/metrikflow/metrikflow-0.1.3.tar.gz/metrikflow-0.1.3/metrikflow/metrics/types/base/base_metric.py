import uuid
import datetime
from pydantic import (
    BaseModel,
    StrictStr, 
    StrictInt,
    StrictFloat
)
from typing import Union, Dict, Any, List, Optional
from .metric_tag import MetricTag
from .metric_types import MetricTypes
from .unit_type import UnitType


class Metric(BaseModel):
    metric_id: StrictStr=str(uuid.uuid4())
    name: StrictStr
    kind: MetricTypes
    group: StrictStr
    timestamp: datetime.datetime
    value: Union[
            StrictInt, 
            StrictFloat
    ]
    tags: List[Dict[StrictStr, StrictStr]]=[]
    unit: Optional[UnitType]=None

    class Config:
        allow_arbitrary_values=True

    @classmethod
    def to_column_names(self):
        return [
            'metric_id',
            'name',
            'kind',
            'group',
            'timestamp',
            'value',
            'unit'
        ]

    @classmethod
    def parse(
        self,
        data: Dict[str, Any]
    ):
        raise Exception('Err. - Parse not implemented on base Metric class.')

    def update(
        self, 
        value: Union[StrictInt, 
            StrictFloat, 
            datetime.datetime, 
            StrictStr
        ]
    ):
        raise NotImplementedError('Err. - Update not implemented on base Metric class.')

    def to_date_string(self):
        return self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f.%z')
    
    def serialize_value(self):
        return self.value

    def to_data_dict(self):
        
        data = {
            key: value for key, value in self.dict().items() if key != 'tags'
        }

        data['timestamp'] = self.to_date_string()
        data['kind'] = self.kind.value

        return data
    
    def to_tags_dict(self):
        tags = {
            key: value for key, value in self.dict().items() if key not in [
                'value', 
                'tags', 
                'timestamp',
                'metric_id'
            ]
        }

        tags['kind'] = self.kind.value

        for tag_set in self.tags:
            tags.update(tag_set)

        return tags
    
    def to_tags(self):
        tags: List[MetricTag] = []

        for tag in self.tags:
            tag_name, tag_value = list(tag.items())[0]

            tags.append(
                MetricTag(
                    name=tag_name,
                    value=tag_value
                )
            )

        return tags
    
    def get_tag(
        self,
        tag_name: str
    ):
        matching_tags = [
            tag for tag in self.tags if tag_name in tag
        ]

        if len(matching_tags) > 0:
            latest_matched_tag = matching_tags[-1]
            tag_name, tag_value = list(latest_matched_tag.items())[0]

            return MetricTag(
                name=tag_name,
                value=tag_value
            )
        
        else:
            return None
    