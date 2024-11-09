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

from .aws_timestream_config import AWSTimestreamConfig
from .aws_timestream_record import AWSTimestreamRecord

try:

    import boto3
    has_connector = True
except Exception:
    has_connector = False

class AWSTimestream:
    has_connector=has_connector

    def __init__(self, config: AWSTimestreamConfig) -> None:
        self.aws_access_key_id = config.aws_access_key_id
        self.aws_secret_access_key = config.aws_secret_access_key
        self.region_name = config.region_name

        self.database_name = config.database_name

        self.retention_options = config.retention_options
        self.session_uuid = str(uuid.uuid4())

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )
        self.query_client = None
        self.write_client = None
        self._loop = asyncio.get_event_loop()
        self.metadata_string: str = None

        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):

        add_signal_handler(
            self._loop,
            handle_loop_stop,
            self._executor,
            self._loop
        )

        self.query_client = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                boto3.client,
                'timestream-query',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        )


        self.write_client = await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                boto3.client,
                'timestream-write',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        )

        try:

            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.write_client.create_database,
                    DatabaseName=self.database_name
                )
            )
 
        except Exception:
            pass

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
        
        try:
            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.write_client.create_table,
                    DatabaseName=self.database_name,
                    TableName=source_name,
                    RetentionProperties=self.retention_options
                )
            )

        except Exception:
           pass

        query = f'SELECT * FROM {self.database_name}.{source_name} WHERE name={metric.name} ORDER BY time DESC'

        try:

            response: Dict[
                str, 
                List[Dict[str, Any]]
            ] = await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.query_client.query,
                    QueryString=query
                )
            )

            column_info = response.get('ColumnInfo', [])
            
            rows = response.get('Rows', [])

            if len(rows) == 0:
                return None
            
            metric_rows: List[Dict[str, Any]] = {}

            for row in rows:
            
                metric_rows: List[
                    Dict[str, Any]
                ] = row.get('Data', [])
                
                metric_data: Dict[str, Any] = {}

                for column, data in zip(column_info, metric_rows):

                    name = column.get('Name')
                    column_type_data: Dict[str, str] = column.get('Type')
                    column_type = column_type_data.get('ScalarType')

                    value = AWSTimestreamRecord.parse_type(
                        column_type,
                        data.get("ScalarValue")
                    )

                    metric_data[name] = value

                metric_rows.append(metric_data)


            metrics: List[Dict[str, Any]] = list(
                sorted(
                    metric_rows,
                    key=lambda metric_data: metric_data.get(
                        'timestamp'
                    )
                )
            )
                
            metric = self._store.parse(
                metrics[-1]
            )

        except Exception:
            pass

        return metric
        
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

        try:
            await self._loop.run_in_executor(
                self._executor,
                functools.partial(
                    self.write_client.create_table,
                    DatabaseName=self.database_name,
                    TableName=destination_name,
                    RetentionProperties=self.retention_options
                )
            )

        except Exception:
           pass

        timestream_record = AWSTimestreamRecord(
            metric,
            self.session_uuid
        )

        await self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self.write_client.write_records,
                DatabaseName=self.database_name,
                TableName=destination_name,
                Records=[
                    timestream_record.to_dict()
                ],
                CommonAttributes={}
            )
        )

    async def close(self):
        self._executor.shutdown(wait=False, cancel_futures=True)