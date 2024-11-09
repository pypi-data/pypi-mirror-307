from metrik.connectors.common.types import ConnectorTypes
from pydantic import BaseModel


class PostgresConfig(BaseModel):
    host: str='localhost'
    database: str
    username: str
    password: str
    reporter_type: ConnectorTypes=ConnectorTypes.Postgres

    class Config:
        arbitrary_types_allowed = True