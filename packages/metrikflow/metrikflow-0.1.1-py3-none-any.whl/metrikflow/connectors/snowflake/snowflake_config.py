from typing import Optional
from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes

class SnowflakeConfig(BaseModel):
    username: str
    password: str
    organization_id: str
    account_id: str
    private_key: Optional[str]
    warehouse: str
    database: str
    database_schema: str='PUBLIC'
    connect_timeout: int=30
    reporter_type: ConnectorTypes=ConnectorTypes.Snowflake

    class Config:
        arbitrary_types_allowed = True