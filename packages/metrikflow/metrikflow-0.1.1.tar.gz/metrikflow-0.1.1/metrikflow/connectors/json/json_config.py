import os
from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes


class JSONConfig(BaseModel):
    overwrite: bool=True
    reporter_type: ConnectorTypes=ConnectorTypes.JSON