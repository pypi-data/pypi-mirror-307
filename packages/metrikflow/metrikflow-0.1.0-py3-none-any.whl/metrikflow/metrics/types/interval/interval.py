import datetime
import time
import uuid
from metrik.metrics.types.base import (
    Metric,
    MetricTypes,
    UnitType
)
from typing import (
    Union, 
    Optional, 
    Dict, 
    Any,
    List
)


class Interval(Metric):

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

        current_time = datetime.datetime.now(
            datetime.timezone.utc
        )

        if value is None:
            value = (
                current_time - timestamp
            ).total_seconds()

        if tags is None:
            tags = []

        super().__init__(
            name=name,
            kind=MetricTypes.INTERVAL,
            group=group,
            timestamp=timestamp,
            value=value,
            tags=tags,
            unit=unit
        )

    @classmethod
    def parse(self, data: Dict[str, Any]):

        return Interval(
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
        
        current_time = datetime.datetime.now(
            datetime.timezone.utc
        )

        value = (
            current_time - self.timestamp
        ).total_seconds()

        update_tags = []
        if tags:
            update_tags = tags
            update_tags.extend(self.tags)

        return Interval(
            metric_id=self.metric_id,
            name=self.name,
            group=self.group,
            timestamp=current_time,
            value=value,
            tags=update_tags,
            unit=self.unit
        )