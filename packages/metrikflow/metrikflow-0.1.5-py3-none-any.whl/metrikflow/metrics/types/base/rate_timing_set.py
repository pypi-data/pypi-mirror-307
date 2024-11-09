from pydantic import (
    BaseModel,
    StrictInt,
    StrictFloat
)
from typing import Union


class RateTimingSet(BaseModel):
    current: StrictFloat=0.0
    last_measured: Union[StrictInt, StrictFloat]
    last_time: StrictFloat