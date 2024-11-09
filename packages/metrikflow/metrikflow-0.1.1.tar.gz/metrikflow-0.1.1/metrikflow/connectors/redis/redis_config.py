from typing import Optional
from metrikflow.connectors.common.types import ConnectorTypes
from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str='localhost:6379'
    username: Optional[str]
    password: Optional[str]
    database: int=0
    secure: bool=False
    reporter_type: ConnectorTypes=ConnectorTypes.Redis