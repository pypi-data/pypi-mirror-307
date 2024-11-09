from pydantic import (
    BaseModel,
    StrictStr
)


class MetricTag(BaseModel):
    name: StrictStr
    value: StrictStr