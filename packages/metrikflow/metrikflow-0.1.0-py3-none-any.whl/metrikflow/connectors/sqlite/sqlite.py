import uuid
from typing import Any, Dict, List, Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .sqlite_config import SQLiteConfig

try:
    import sqlalchemy
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.schema import CreateTable
    
    has_connector = True

except Exception:
    ASYNCIO_STRATEGY = None
    sqlalchemy = None
    CreateTable = None
    OperationalError = None
    has_connector = False



class SQLite:
    has_connector=has_connector

    def __init__(self, config: SQLiteConfig) -> None:
        self.path = f'sqlite+aiosqlite:///{config.path}'
        self.events_table_name = config.events_table
        self.metrics_table_name = config.metrics_table

        self.metadata = sqlalchemy.MetaData()

        self.database = None
        self._engine = None
        self._connection = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):
        self._engine = create_async_engine(self.path)

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
            sqlalchemy.Column('value', sqlalchemy.Float())
        ) 


        metrics_data: List[Dict[str, Any]] = []

        async with self._engine.begin() as connection:
            
            await connection.execute(
                CreateTable(
                    table,
                    if_not_exists=True
                )
            )

            results = await connection.execute(
                table.select().where(
                    table.c.name == metric.name
                ).order_by(
                    table.c.timestamp.desc()
                ).limit(1)
            )

            for row in results.fetchall():
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
            sqlalchemy.Column('timestamp', sqlalchemy.TEXT()),
            sqlalchemy.Column('value', sqlalchemy.Float())
        ) 
        
        async with self._engine.begin() as connection:

            await connection.execute(
                CreateTable(
                    table,
                    if_not_exists=True
                )
            )

            async with connection.begin() as transaction:

                metric_data = metric.dict()
                metric_data['kind'] = metric.kind.value

                await connection.execute(
                    table.insert().values(
                        **metric_data
                    )
                )   

                await transaction.commit()
    
    async def close(self):
        await self._engine.dispose()