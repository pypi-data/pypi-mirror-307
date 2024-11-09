import uuid
from typing import Union

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate
from metrikflow.metrics.types.base import MetricTypes

from .datadog_config import DatadogConfig
from .units import DatadogUnitMap

try:
    # Datadog uses aiosonic
    from aiosonic import HTTPClient, TCPConnector, Timeouts
    from datadog_api_client import AsyncApiClient, Configuration
    from datadog_api_client.v2.api.metrics_api import MetricPayload, MetricsApi
    from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
    from datadog_api_client.v2.model.metric_point import MetricPoint
    from datadog_api_client.v2.model.metric_resource import MetricResource
    from datadog_api_client.v2.model.metric_series import MetricSeries

    has_connector = True

except Exception:
    HTTPClient=None
    TCPConnector=None
    Timeouts=None
    MetricsApi=None
    MetricPayload=None
    MetricSeries=None
    AsyncApiClient=None
    Configuration=None
    MetricPoint=None
    MetricIntakeType=None
    datadog = None
    has_connector = False


class Datadog:
    has_connector=has_connector

    def __init__(self, config: DatadogConfig) -> None:
        self.datadog_api_key = config.api_key
        self.datadog_app_key = config.app_key
        self.device_name = config.device_name
        self.server_location = config.server_location
        self.priority = config.priority
        self.custom_fields = config.custom_fields or {}

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()
        
        self._config = None
        self._client = None
        self.metrics_api = None
        self.metric_types_map = {
            MetricTypes.INTERVAL: MetricIntakeType.GAUGE,
            MetricTypes.RATE: MetricIntakeType.RATE,
            MetricTypes.EVENT: MetricIntakeType.GAUGE
        }

        self._units_map = DatadogUnitMap()

    async def connect(self):

        self._config = Configuration()
        self._config.api_key["apiKeyAuth"] = self.datadog_api_key
        self._config.api_key["appKeyAuth"] = self.datadog_app_key

        if self.server_location:
            self._config.server_variables["site"] = self.server_location

        self._client = AsyncApiClient(self._config)

        # Datadog's implementation of aiosonic's HTTPClient lacks a lot
        # of configurability, incuding actually being able to set request timeouts
        # so we substitute our own implementation.

        tcp_connection = TCPConnector(timeouts=Timeouts(sock_connect=30))
        self._client.rest_client._client = HTTPClient(tcp_connection)

        self.metrics_api = MetricsApi(self._client)

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
        raise Exception('Err. - Datadog connector is send only.')
        

    async def send(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60
    ):

        metric_name = f'{metric.group}.{metric.name}'

        metric_tags = [
            f'{tag_name}:{tag_value}' for tag_name, tag_value in metric.to_tags_dict().items()
        ]

        metric_tags.append(
            f'group:{metric.group}'
        )
        
        series = MetricSeries(
            metric_name, 
            [MetricPoint(
                timestamp=int(metric.timestamp.timestamp()),
                value=metric.value
            )],
            type=self.metric_types_map.get(
                metric.kind,
                MetricIntakeType.GAUGE
            ),
            tags=metric_tags,
            resources=[
                MetricResource(
                    name=self.device_name,
                    type='host'
                )
            ],
            unit=self._units_map.get(metric.unit)
        )

        response = await self.metrics_api.submit_metrics(
            body=MetricPayload(
                series=[series]
            )
        )

        if len(response.errors) > 0:
            for error in response.errors:
                raise Exception(error)
        
    async def close(self):
        pass