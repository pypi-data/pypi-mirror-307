import os
from pydantic import BaseModel
from metrik.connectors.common.types import ConnectorTypes


class CSVConfig(BaseModel):
    overwrite: bool=True
    reporter_type: ConnectorTypes=ConnectorTypes.CSV