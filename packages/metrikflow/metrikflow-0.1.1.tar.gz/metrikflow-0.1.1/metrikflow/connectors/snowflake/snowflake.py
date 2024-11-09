import asyncio
import functools
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Union

from metrikflow.connectors.common.signals import add_signal_handler, handle_loop_stop
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics import MetricStore
from metrikflow.metrics.types import Event, Interval, Rate

from .snowflake_config import SnowflakeConfig

try:
    import sqlalchemy
    from snowflake.sqlalchemy import URL
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable
    
    has_connector = True

except Exception:
    snowflake = None
    has_connector = False

class Snowflake:
    has_connector=has_connector

    def __init__(self, config: SnowflakeConfig) -> None:
        self.username = config.username
        self.password = config.password
        self.organization_id = config.organization_id
        self.account_id = config.account_id
        self.private_key = config.private_key
        self.warehouse = config.warehouse
        self.database = config.database
        self.schema = config.database_schema

        self.connect_timeout = config.connect_timeout
        
        self.metadata = sqlalchemy.MetaData()
        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )

        self._engine = None
        self._connection = None

        self._loop = asyncio.get_event_loop()

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()
        self._store = MetricStore()

    async def connect(self):

        try:

            add_signal_handler(
                self._loop,
                handle_loop_stop,
                self._executor,
                self._loop
            )
            
            self._engine = await self._loop.run_in_executor(
                self._executor,
                create_engine,
                URL(
                    user=self.username,
                    password=self.password,
                    account=self.account_id,
                    warehouse=self.warehouse,
                    database=self.database,
                    schema=self.schema
                )
            
            )

            self._connection = await asyncio.wait_for(
                self._loop.run_in_executor(
                    self._executor,
                    self._engine.connect
                ),
                timeout=self.connect_timeout
            )

        except asyncio.TimeoutError:
            raise Exception('Err. - Connection to Snowflake timed out - check your account id, username, and password.')
        
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

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._connection.execute,
                CreateTable(
                    table, 
                    if_not_exists=True
                )
            )
        )

        rows: List[Any] = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._connection.execute,
                table.select().where(
                    table.c.name == metric.name
                ).order_by(
                    table.c.timestamp.desc()
                ).limit(1)
            )
        )

        metrics_data: List[Dict[str, Any]] = []
        for row in rows:
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

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._connection.execute,
                CreateTable(
                    table, 
                    if_not_exists=True
                )
            )
        )

        metric_data = metric.dict()
        metric_data['kind'] = metric.kind.value

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._connection.execute,
                table.insert().values(**metric_data)
            )
        )

    async def close(self):

        await self._loop.run_in_executor(
            self._executor,
            self._connection.close
        )

        self._executor.shutdown(wait=False, cancel_futures=True)
