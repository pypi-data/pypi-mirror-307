from typing import Dict, Optional
from pydantic import (
    BaseModel,
    StrictStr
)
from metrikflow.connectors.common.types import ConnectorTypes


class DatadogConfig(BaseModel):
    api_key: StrictStr
    app_key: StrictStr
    device_name: Optional[StrictStr]=None
    server_location: Optional[StrictStr]=None
    priority: StrictStr='normal'
    reporter_type: ConnectorTypes=ConnectorTypes.Datadog