import datetime
from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool
)
from typing import Optional, Literal


class DatadogDashboardSummary(BaseModel):
    author_handle: StrictStr
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]=None
    description: Optional[StrictStr]=None
    id: StrictStr
    is_read_only: StrictBool
    layout_type: Literal[
        "ordered",
        "free"
    ]
    modified_at: datetime.datetime
    title: StrictStr
    url: StrictStr

    @classmethod
    def fields(cls):
        return [
            'author_handle',
            'created_at',
            'deleted_at',
            'description',
            'id',
            'is_read_only',
            'layout_type',
            'modified_at',
            'title',
            'url'
        ]