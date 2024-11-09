import datetime
from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Union, Optional, Literal
from .types.base import MetricTypes


class MetricQuery(BaseModel):
    name: Optional[StrictStr]=None
    kind: Optional[
        Union[
            Literal['event'],
            Literal['interval'],
            Literal['rate']
        ]
    ]=None,
    group: Optional[StrictStr]=None
    newer_than: Optional[datetime.datetime]=None
    older_than: Optional[datetime.datetime]=None

