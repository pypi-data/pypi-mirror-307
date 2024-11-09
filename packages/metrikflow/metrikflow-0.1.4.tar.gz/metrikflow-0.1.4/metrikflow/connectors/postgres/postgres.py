# # This is an ugly patch for: https://github.com/aio-libs/aiopg/issues/837
# import selectors  # isort:skip # noqa: F401

# selectors._PollLikeSelector.modify = (  # type: ignore
#     selectors._BaseSelectorImpl.modify  # type: ignore
# )

import uuid
from typing import Any, Dict, List, Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .postgres_config import PostgresConfig

try:
    import sqlalchemy
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio.engine import (
        AsyncConnection,
        AsyncEngine,
        AsyncTransaction,
    )
    from sqlalchemy.schema import CreateTable
    
    has_connector = True

except Exception:
    UUID = None
    sqlalchemy = None
    create_engine = None
    has_connector = False


class Postgres:
    has_connector=has_connector

    def __init__(self, config: PostgresConfig) -> None:
        self.host = config.host
        self.database = config.database
        self.username = config.username
        self.password = config.password

        self._engine = None
        self.metadata = sqlalchemy.MetaData()

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()
        self.sql_type = 'Postgresql'

        self._store = MetricStore()

    async def connect(self):
  
        connection_uri = 'postgresql+asyncpg://'

        if self.username and self.password:
            connection_uri = f'{connection_uri}{self.username}:{self.password}@'

        self._engine: AsyncEngine = await create_async_engine(
            f'{connection_uri}{self.host}/{self.database}',
            echo=False
        )

    async def load(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60       
    ):
        
        table = sqlalchemy.Table(
            source_name,
            self.metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('metric_id', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('name', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('kind', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('group', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('timestamp', sqlalchemy.DateTime()),
            sqlalchemy.Column('value', sqlalchemy.Float()),
        )   


        metrics_data: List[Dict[str, Any]] = []

        async with self._engine.connect() as connection:
            connection: AsyncConnection = connection

            await connection.execute(
                CreateTable(
                    table,
                    if_not_exists=True
                )
            )

            async for row in connection.execute(
               table.select().where(
                  table.c.name == metric.name
               ).order_by(
                  table.c.timestamp.desc()
               ).limit(1)
            ):
                metrics_data.append({
                    'metric_id': row.metric_id,
                    'name': row.name,
                    'kind': row.kind,
                    'group': row.group,
                    'timestamp': row.timestamp,
                    'value': row.value
                })

        return self._store.parse(
            metrics_data[-1]
        )

    async def send(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60      
    ):

        table = sqlalchemy.Table(
            destination_name,
            self.metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('metric_id', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('name', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('kind', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('group', sqlalchemy.VARCHAR(255)),
            sqlalchemy.Column('timestamp', sqlalchemy.DateTime()),
            sqlalchemy.Column('value', sqlalchemy.Float())
        )   

        async with self._engine.connect() as connection:
            connection: AsyncConnection = connection

            await connection.execute(
                CreateTable(
                    table,
                    if_not_exists=True
                )
            )

            async with connection.begin() as transaction:
                transaction: AsyncTransaction = transaction

                metric_data = metric.dict()
                metric_data['kind'] = metric.kind.value

                await connection.execute(
                    table.insert().values(**metric_data)
                )

                await transaction.commit()

    async def close(self):
        pass



    
