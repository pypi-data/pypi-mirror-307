from typing import Dict
from metrikflow.connectors.common.types import ConnectorTypes
from pydantic import BaseModel


class DogStatsDConfig(BaseModel):
    host: str='localhost'
    port: int=8125
    custom_fields: Dict[str, str]={}
    reporter_type: ConnectorTypes=ConnectorTypes.DogStatsD