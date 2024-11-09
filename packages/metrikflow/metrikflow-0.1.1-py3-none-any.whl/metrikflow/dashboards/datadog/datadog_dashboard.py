# Datadog uses aiosonic
from aiosonic import HTTPClient, TCPConnector, Timeouts
from datadog_api_client import (
    AsyncApiClient, 
    Configuration
)
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_summary import DashboardSummary
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.widget import Widget
from metrikflow.metrics.types import (
    Event,
    Interval,
    Rate
)
from typing import List, Union, Literal, Optional, Dict, Any
from .datadog_config import DatadogConfig
from .models import (
    DatadogDashboardSummary,
    WidgetMetric, 
    WidgetOptions
)
from .widgets import WidgetsFactory

class DatadogDashboard:

    def __init__(self, config: DatadogConfig) -> None:
        self.datadog_api_key = config.api_key
        self.datadog_app_key = config.app_key
        self.device_name = config.device_name
        self.server_location = config.server_location
        self.priority = config.priority

        self._widgets: List[Widget] = []
        self._config: Union[Configuration, None] = None
        self._client: Union[AsyncApiClient, None] = None
        self._dashboards_api: Union[DashboardsApi, None] = None
        self._widgets_factory = WidgetsFactory()
        self._summaries: Dict[str, DatadogDashboardSummary] = {}
        self._summary_titles: Dict[str, str] = {}
        self._title_id_map: Dict[str, str] = {}

    @property
    def ids(self):
        return list(self._summary_titles.keys())

    @property
    def names(self):
        return list(self._summary_titles.values())
    
    def get_id_by_title(
        self,
        title: str
    ):
        return self._title_id_map.get(title)

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

        self._dashboards_api = DashboardsApi(self._client)

    def add_metric(
        self,
        widget: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],
        kind: Literal[
            'change',
            'histogram',
            'query_value',
            'scatter_plot',
            'table',
            'timeseries'
        ]='timeseries',
        size: Union[
            Literal['extra_small'],
            Literal['small'],
            Literal['medium'],
            Literal['large'],
            Literal['extra_large']
        ]='medium',
        aggregator: Union[
            Literal['average'],
            Literal['total'],
            Literal['maximum'],
            Literal['minimum']
        ]='average',
        aggregator_field: Optional[str]=None,
        options: Optional[WidgetOptions]=None
    ):
        self._widgets_factory.add_metric(
            WidgetMetric(
                widget_name=widget,
                widget_type=kind,
                metric=metric,
                widget_size=size,
                widget_aggregator=aggregator,
                widget_aggregator_field=aggregator_field,
                widget_options=options
            )
        )

    async def create_dashboard(
        self,
        title: str,
        description: str,
        options: Optional[WidgetOptions]=None
    ) -> Dashboard:
        widgets = self._widgets_factory.to_widgets(options=options)
        dashboard = Dashboard(
            title=title,
            description=description,
            widgets=widgets,
            layout_type=DashboardLayoutType.ORDERED
        )

        response: Dashboard = await self._dashboards_api.create_dashboard(dashboard)
        self._store_dashboard_as_summary(response)

        return response
    
    async def get_dashboard(
        self,
        dashboard_id: str
    ) -> Dashboard:
        
        response: Dashboard = await self._dashboards_api.get_dashboard(dashboard_id)
        self._store_dashboard_as_summary(response)

        return response
    
    async def list_api_dashboards(
        self,
        limit: int=50,
        offset: int=0,
        hide_shared: bool=False,
        hide_deleted: bool=False
    ):
        response: DashboardSummary = await self._dashboards_api.list_dashboards(
            filter_shared=hide_shared,
            filter_deleted=hide_deleted,
            count=limit,
            start=offset
        )

        dashboards = [
            DatadogDashboardSummary(
                **dashboard
            ) for dashboard in response.to_dict().get('dashboards', [])
        ]

        for dashboard in dashboards:
            self._summaries[dashboard.id] = dashboard
            self._summary_titles[dashboard.id] = dashboard.title
            self._title_id_map[dashboard.title] = dashboard.id

        return dashboards
    
    async def list_all_api_dashboards(
        self,
        limit: int=100
    ):
        
        discovered = await self.list_api_dashboards(
            limit=limit
        )

        discovered_count = len(discovered)
        offset = discovered_count
        
        while discovered_count == limit:
            discovered = await self.list_api_dashboards(
                offset=offset
            )

            discovered_count = len(discovered)
            offset += discovered_count

        return list(self._summaries.values())
    
    async def update_dashboard(
        self,
        dashboard_id: str,
        title: str,
        description: str,
        options: Optional[WidgetOptions]=None
    ):
        
        widgets = self._widgets_factory.to_widgets(options=options)
        dashboard = Dashboard(
            title=title,
            description=description,
            widgets=widgets,
            layout_type=DashboardLayoutType.ORDERED
        )

        return await self._dashboards_api.update_dashboard(
            dashboard_id,
            dashboard
        )
    
    async def delete_dashboard(
        self,
        dashboard_id: str
    ):
        return await self._dashboards_api.delete_dashboard(
            dashboard_id
        )

    def _store_dashboard_as_summary(
        self,
        dashboard: Dashboard
    ) -> DashboardSummary:
        dashboard_summary_data = {
            key: value for key, value in dashboard.to_dict().items() if key in DatadogDashboardSummary.fields()
        }

        dashboard_summary = DatadogDashboardSummary(**dashboard_summary_data)
        self._summaries[dashboard_summary.id] = dashboard_summary
        self._summary_titles[dashboard_summary.id] = dashboard_summary.title
        self._title_id_map[dashboard.title] = dashboard_summary.id

        return dashboard_summary