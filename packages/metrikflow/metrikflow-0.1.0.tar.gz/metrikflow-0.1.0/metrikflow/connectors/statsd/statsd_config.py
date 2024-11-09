from typing import Dict
from pydantic import BaseModel
from metrik.connectors.common.types import ConnectorTypes


class StatsDConfig(BaseModel):
    host: str='localhost'
    port: int=8125
    reporter_type: ConnectorTypes=ConnectorTypes.StatsD