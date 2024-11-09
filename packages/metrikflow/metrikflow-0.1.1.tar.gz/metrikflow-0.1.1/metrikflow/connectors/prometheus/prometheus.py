import asyncio
import functools
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Union

from metrikflow.connectors.common.signals import add_signal_handler, handle_loop_stop
from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate
from metrikflow.metrics.types.base import MetricTypes

try:
    from prometheus_client import (
        CollectorRegistry,
        push_to_gateway,
    )
    from prometheus_client.core import REGISTRY
    from prometheus_client.exposition import basic_auth_handler

    from .prometheus_config import PrometheusConfig
    from .prometheus_metric import PrometheusMetric
    has_connector = True

except Exception:
    PrometheusConfig = None
    has_connector = False
    basic_auth_handler = lambda: None



class Prometheus:
    has_connector=has_connector

    def __init__(self, config: PrometheusConfig) -> None:
        self.pushgateway_address = config.pushgateway_address
        self.auth_request_method = config.auth_request_method
        self.auth_request_timeout = config.auth_request_timeout
        self.auth_request_data = config.auth_request_data
        self.username = config.username
        self.password = config.password
        self.namespace = config.namespace
        self.job_name = config.job_name

        self.registry = None
        self._auth_handler = None
        self._has_auth = False
        self._loop = asyncio.get_event_loop()


        self._metrics: Dict[str, PrometheusMetric] = {}

        self.metric_types_map = {
            MetricTypes.EVENT: 'gauge',
            MetricTypes.INTERVAL: 'gauge',
            MetricTypes.RATE: 'gauge'
        }

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikflowLogger()
        self.logger.initialize()

        self._executor = ThreadPoolExecutor(
            max_workers=os.cpu_count()
        )
        
    async def connect(self) -> None:

        self.registry = CollectorRegistry()
        REGISTRY.register(self.registry)

        if self.username and self.password:
            self._has_auth = True   

        add_signal_handler(
            self._loop,
            handle_loop_stop,
            self._executor,
            self._loop
        )   

    def _generate_auth(self) -> basic_auth_handler:
        return basic_auth_handler(
            self.pushgateway_address,
            self.auth_request_method,
            self.auth_request_timeout,
            {
                'Content-Type': 'application/json'
            },
            self.auth_request_data,
            username=self.username,
            password=self.password
        )
    
    async def _submit_to_pushgateway(
        self,
        pushgateway_address: str
    ):
        
        self.pushgateway_address = pushgateway_address

        if self._has_auth:

            await self._loop.run_in_executor(
                None,
                functools.partial(
                    push_to_gateway,
                    self.pushgateway_address,
                    job=self.job_name,
                    registry=self.registry,
                    handler=self._generate_auth
                )
            )

        else:
            await self._loop.run_in_executor(
                None,
                functools.partial(
                    push_to_gateway,
                    self.pushgateway_address,
                    job=self.job_name,
                    registry=self.registry
                )
            )

    async def load(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        timeout: Union[int, float]=60         
    ):
        raise Exception('Err. - Prometheus connector is send only.')
        

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
        tags_dict = metric.to_tags_dict()

        tags: List[str] = [
            f'{tag_name}:{tag_value}' for tag_name, tag_value in tags_dict.items()
        ]

        prometheus_metric = self._metrics.get(metric.name)

        if prometheus_metric is None:

            metric_type = self.metric_types_map.get(metric.kind, 'gauge')

            prometheus_metric = PrometheusMetric(
                metric.name,
                metric_type,
                metric_description=f'{metric.name} {metric.group}',
                metric_labels=tags,
                metric_namespace=self.namespace,
                registry=self.registry
            )
            prometheus_metric.create_metric()

        prometheus_metric.update(
            value=metric.value,
            labels=tags
        )

        await self._submit_to_pushgateway(
            destination_name
        )

    async def close(self):
        self._executor.shutdown(wait=False, cancel_futures=True)       