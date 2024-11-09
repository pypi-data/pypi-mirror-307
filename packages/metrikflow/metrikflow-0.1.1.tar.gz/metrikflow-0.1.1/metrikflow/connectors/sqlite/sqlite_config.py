import os
from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes


class SQLiteConfig(BaseModel):
    path: str=f'{os.getcwd()}/results.db'
    reporter_type: ConnectorTypes=ConnectorTypes.SQLite

    class Config:
        arbitrary_types_allowed = True