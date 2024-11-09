import datetime
import time
import uuid
from typing import (
    Union, 
    Optional, 
    Dict, 
    Any,
    List
)
from metrik.metrics.types.base import (
    Metric,
    MetricTypes,
    UnitType
)


class Rate(Metric):

    def __init__(
        self,
        metric_id: str=None,
        name: str=None,
        group: str=None,
        timestamp: datetime.datetime=None,
        value: Union[int, float]=None,
        tags: Optional[
            List[
                Dict[str, str]
            ]
        ]=None,
        unit: Optional[UnitType]=None
    ):
        if metric_id is None:
            metric_id = str(uuid.uuid4())
        
        if value is None:
            value = 1
        
        if tags is None:
            tags = []
  
        super().__init__(
            name=name,
            kind=MetricTypes.RATE,
            group=group,
            timestamp=timestamp,
            value=value,
            tags=tags,
            unit=unit
        )

    @classmethod
    def parse(self, data: Dict[str, Any]):

        return Rate(
            metric_id=data.get('metric_id'),
            name=data.get('name'),
            group=data.get('group'),
            timestamp=data.get('timestamp'),
            value=data.get('value'),
            tags=data.get('tags'),
            unit=data.get('unit')
        )

    def update(
        self,
        value: Union[
            int,
            float,
            datetime.datetime,
            str
        ],
        tags: Optional[
            List[
                Dict[str, str]
            ]
        ]=None
    ):
        if value is None:
            value = 1

        update_tags = []
        if tags:
            update_tags = tags
            update_tags.extend(self.tags)

        return Rate(
            metric_id=self.metric_id,
            name=self.name,
            group=self.group,
            timestamp=self.timestamp,
            value=self.calculate_rate(value),
            tags=update_tags,
            unit=self.unit
        )
    
    def calculate_rate(
        self,
        value: Union[int, float]
    ) -> Union[int, float]:

        return (
            value + self.value
        )/(
            datetime.datetime.now(
                datetime.timezone.utc
            ) - self.timestamp
        ).seconds