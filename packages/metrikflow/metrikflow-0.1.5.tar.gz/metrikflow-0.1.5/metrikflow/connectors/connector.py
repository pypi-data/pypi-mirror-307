import asyncio
from metrikflow.metrics.types import (
    Event,
    Interval,
    Rate
)
from typing import Dict, Union, Callable, Any, Literal
from .aws_lambda import (
    AWSLambda,
    AWSLambdaConfig
)
from .aws_timestream import (
    AWSTimestream,
    AWSTimestreamConfig
)
from .cloudwatch import (
    Cloudwatch,
    CloudwatchConfig
)
from .common import ConnectorTypes
from .csv import (
    CSV,
    CSVConfig
)
from .datadog import (
    Datadog,
    DatadogConfig
)
from .dogstatsd import (
    DogStatsD,
    DogStatsDConfig
)
from .json import (
    JSON,
    JSONConfig
)
from .kafka import (
    Kafka,
    KafkaConfig
)
from .mysql import (
    MySQL,
    MySQLConfig
)
from .postgres import (
    Postgres,
    PostgresConfig
)
from .prometheus import (
    Prometheus,
    PrometheusConfig
)
from .redis import (
    Redis,
    RedisConfig
)
from .s3 import (
    S3,
    S3Config
)
from .snowflake import (
    Snowflake,
    SnowflakeConfig
)
from .sqlite import (
    SQLite,
    SQLiteConfig
)
from .statsd import (
    StatsD,
    StatsDConfig
)
from .xml import (
    XML,
    XMLConfig
)


ConnectorConfig = Union[
    AWSLambdaConfig,
    AWSTimestreamConfig,
    CloudwatchConfig,
    CSVConfig,
    DatadogConfig,
    DogStatsDConfig,
    JSONConfig,
    KafkaConfig,
    MySQLConfig,
    PostgresConfig,
    PrometheusConfig,
    RedisConfig,
    S3Config,
    SnowflakeConfig,
    SQLiteConfig,
    StatsDConfig,
    XMLConfig
]

ConnectorInstance = Union[
    AWSLambda,
    AWSTimestream,
    Cloudwatch,
    CSV,
    Datadog,
    DogStatsD,
    JSON,
    Kafka,
    MySQL,
    Postgres,
    Prometheus,
    Redis,
    S3,
    Snowflake,
    SQLite,
    StatsD,
    XML
]


ConnectorTypeName = Union[
    Literal['aws-lambda'],
    Literal['aws-timestream'],
    Literal['cloudwatch'],
    Literal['csv'],
    Literal['datadog'],
    Literal['dogstatsd'],
    Literal['json'],
    Literal['kafka'],
    Literal['mysql'],
    Literal['postgres'],
    Literal['prometheus'],
    Literal['redis'],
    Literal['s3'],
    Literal['snowflake'],
    Literal['sqlite'],
    Literal['statsd'],
    Literal['xml']
]


class Connector:

    def __init__(self) -> None:
        
        self._connectors: Dict[
            ConnectorTypes,
            Callable[
                [ConnectorConfig],
                ConnectorInstance
            ]
        ] = {
            ConnectorTypes.AWSLambda: lambda config: AWSLambda(config),
            ConnectorTypes.AWSTimestream: lambda config: AWSTimestream(config),
            ConnectorTypes.Cloudwatch: lambda config: Cloudwatch(config),
            ConnectorTypes.CSV: lambda config: CSV(config),
            ConnectorTypes.Datadog: lambda config: Datadog(config),
            ConnectorTypes.DogStatsD: lambda config: DogStatsD(config),
            ConnectorTypes.JSON: lambda config: JSON(config),
            ConnectorTypes.Kafka: lambda config: Kafka(config),
            ConnectorTypes.MySQL: lambda config: MySQL(config),
            ConnectorTypes.Postgres: lambda config: Postgres(config),
            ConnectorTypes.Prometheus: lambda config: Prometheus(config),
            ConnectorTypes.Redis: lambda config: Redis(config),
            ConnectorTypes.S3: lambda config: S3(config),
            ConnectorTypes.Snowflake: lambda config: Snowflake(config),
            ConnectorTypes.SQLite: lambda config: SQLite(config),
            ConnectorTypes.StatsD: lambda config: StatsD(config),
            ConnectorTypes.XML: lambda config: XML(config)

        }



        self._configs: Dict[
            ConnectorTypes,
            Callable[
                [Dict[str, Any]],
                ConnectorConfig
            ]
        ] = {
            ConnectorTypes.AWSLambda: lambda config: AWSLambdaConfig(
                **config
            ),
            ConnectorTypes.AWSTimestream: lambda config: AWSTimestreamConfig(
                **config
            ),
            ConnectorTypes.Cloudwatch: lambda config: CloudwatchConfig(
                **config
            ),
            ConnectorTypes.CSV: lambda config: CSVConfig(
                **config
            ),
            ConnectorTypes.Datadog: lambda config: DatadogConfig(
                **config
            ),
            ConnectorTypes.DogStatsD: lambda config: DogStatsDConfig(
                **config
            ),
            ConnectorTypes.JSON: lambda config: JSONConfig(
                **config
            ),
            ConnectorTypes.Kafka: lambda config: KafkaConfig(
                **config
            ),
            ConnectorTypes.MySQL: lambda config: MySQLConfig(
                **config
            ),
            ConnectorTypes.Postgres: lambda config: PostgresConfig(
                **config
            ),
            ConnectorTypes.Prometheus: lambda config: PrometheusConfig(
                **config
            ),
            ConnectorTypes.Redis: lambda config: RedisConfig(
                **config
            ),
            ConnectorTypes.S3: lambda config: S3Config(
                **config
            ),
            ConnectorTypes.Snowflake: lambda config: SnowflakeConfig(
                **config
            ),
            ConnectorTypes.SQLite: lambda config: SQLiteConfig(
                **config
            ),
            ConnectorTypes.StatsD: lambda config: StatsDConfig(
                **config
            ),
            ConnectorTypes.XML: lambda config: XMLConfig(
                **config
            )
        }

        self._types: Dict[str, ConnectorTypes] = {
            'aws-lambda': ConnectorTypes.AWSLambda,
            'aws-timestream': ConnectorTypes.AWSTimestream,
            'cloudwatch': ConnectorTypes.Cloudwatch,
            'csv': ConnectorTypes.CSV,
            'datadog': ConnectorTypes.Datadog,
            'dogstatsd': ConnectorTypes.DogStatsD,
            'json': ConnectorTypes.JSON,
            'kafka': ConnectorTypes.Kafka,
            'mysql': ConnectorTypes.MySQL,
            'postgres': ConnectorTypes.Postgres,
            'prometheus': ConnectorTypes.Prometheus,
            'redis': ConnectorTypes.Redis,
            's3': ConnectorTypes.S3,
            'snowflake': ConnectorTypes.Snowflake,
            'sqlite': ConnectorTypes.SQLite,
            'statsd': ConnectorTypes.StatsD,
            'xml': ConnectorTypes.XML
        }

        self.selected_connector: Union[
            ConnectorInstance,
            None
        ] = None

        self.selected_connector_config: Union[
            ConnectorConfig,
            None
        ] = None

        self.selected_connector_type: Union[
            ConnectorTypes,
            None
        ] = None

        self._loop: Union[
            asyncio.AbstractEventLoop,
            None
        ] = None

    def select(
        self,
        connector_type: str,
        **kwargs
    ):
        
        self.selected_connector_type = self._types.get(connector_type)

        if self.selected_connector_type is None:
            raise Exception(
                f'Err. - no Connector of type - {connector_type} - exists.'
            )

        self.selected_connector_config = self._configs.get(
            self.selected_connector_type
        )(kwargs)

        self.selected_connector = self._connectors.get(
            self.selected_connector_type
        )(self.selected_connector_config)

    def load(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        return self._loop.run_until_complete(
            self._load(
                source_name,
                metric
            )
        )

    async def _load(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):
        await self.selected_connector.connect()
        result = await self.selected_connector.load(
            source_name,
            metric,
            timeout=timeout
        )

        await self.selected_connector.close()

        return result

    def send(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60        
    ):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        return self._loop.run_until_complete(
            self._send(
                destination_name,
                metric,
                timeout=timeout
            )
        )
    
    async def _send(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60      
    ):
        await self.selected_connector.connect()
        await self.selected_connector.send(
            destination_name,
            metric,
            timeout=timeout
        )

        await self.selected_connector.close()
