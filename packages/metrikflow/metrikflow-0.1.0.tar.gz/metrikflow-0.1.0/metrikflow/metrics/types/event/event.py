from __future__ import annotations
import datetime
import uuid
from typing import (
    Any, 
    Dict, 
    Union, 
    Optional, 
    List
)

from pydantic import StrictFloat, StrictInt, StrictStr
from metrik.metrics.types.base import (
    Metric,
    MetricTypes,
    UnitType
)


class Event(Metric):

    def __init__(
        self,
        metric_id: str=None,
        name: str=None,
        group: str=None,
        timestamp: datetime.datetime=None,
        value: Union[
            int,
            float,
            datetime.datetime,
            str
        ]=None,
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
            kind=MetricTypes.EVENT,
            group=group,
            timestamp=timestamp,
            value=value,
            tags=tags,
            unit=unit
        )

    @classmethod
    def parse(self, data: Dict[str, Any]):
        return Event(
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

        return Event(
            metric_id=self.metric_id,
            name=self.name,
            group=self.group,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),
            value=value,
            tags=update_tags,
            unit=self.unit
        )