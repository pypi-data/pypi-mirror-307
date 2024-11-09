from typing import (
    Dict,
    Callable
)
from .datadog import (
    DatadogDashboardFactory,
    DatadogConfig,
    DatadogDashboard
)
from .datadog.models.widget_options import WidgetOptions
from typing import Any
from .common import DashboardType


class Dashboard:

    def __init__(
        self
    ) -> None:
        self._factories: Dict[
            DashboardType.DATADOG,
            DatadogDashboardFactory
        ] = {}

        self._dashboards: Dict[
            str,
            DatadogDashboard
        ] = {}

    def __getitem__(
        self,
        dashboard_name: str
    ):
        return self._dashboards.get(dashboard_name)
    
    def get(
        self,
        dashboard_name: str
    ):
        return self._dashboards.get(dashboard_name)

    async def create_datadog_dashboard(
        self,
        config: Dict[
            str,
            Any
        ],
        dashboard_name: str
    ):
        if self._factories.get(DashboardType.DATADOG) is None:
            self._factories[DashboardType.DATADOG] = DatadogDashboardFactory(
                DatadogConfig(**config)
            )

        new_dashboard = self._factories[DashboardType.DATADOG].get(dashboard_name)

        await new_dashboard.connect()

        self._dashboards[dashboard_name] = new_dashboard

        return new_dashboard
    
    async def publish(
        self,
        dashboard_name: str,
        description: str,
        options: WidgetOptions=None
    ):
        return await self._dashboards[dashboard_name].create_dashboard(
            dashboard_name,
            description,
            options=options
        )