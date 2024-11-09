from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes



class MySQLConfig(BaseModel):
    host: str='127.0.0.1'
    database: str
    username: str
    password: str
    reporter_type: ConnectorTypes=ConnectorTypes.MySQL

    class Config:
        arbitrary_types_allowed = True