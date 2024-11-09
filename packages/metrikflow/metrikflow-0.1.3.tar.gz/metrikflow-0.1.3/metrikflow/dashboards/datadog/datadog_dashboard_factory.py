from collections import defaultdict
from typing import Dict
from .datadog_dashboard import DatadogDashboard
from .datadog_config import DatadogConfig


class DatadogDashboardFactory:

    def __init__(
        self,
        config: DatadogConfig
    ) -> None:
        self._config = config
        self._dashboards: Dict[
            str,
            DatadogDashboard
        ] = defaultdict(
            lambda: DatadogDashboard(self._config)
        )

    def __getitem__(self, dashboard_name: str):
        return self._dashboards[dashboard_name]
    
    def get(self, dashboard_name: str):
        return self._dashboards[dashboard_name]