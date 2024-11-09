from .dashboard_type import DashboardType


class DashboardTypeMap:

    def __init__(self) -> None:
        self._types = {
            'datadog': DashboardType.DATADOG
        }

    def __iter__(self):
        for dashboard_type in self._types.values():
            yield dashboard_type

    def __getitem__(self, dashboard_type: str):
        return self._types.get(
            dashboard_type,
            DashboardType.DATADOG
        )
    
    def get(self, dashboard_type: str):
        return self._types.get(dashboard_type)