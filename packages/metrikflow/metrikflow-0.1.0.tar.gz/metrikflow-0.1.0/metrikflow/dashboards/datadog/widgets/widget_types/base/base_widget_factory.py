from collections import defaultdict
from metrik.dashboards.datadog.layouts.size_type import SizeType
from metrik.dashboards.datadog.models import (
    Query,
    WidgetType
)
from typing import Literal, List, Dict, TypeVar, Generic

T = TypeVar('T')


class BaseWidgetFactory(Generic[T]):

    def __init__(
        self,
        kind: WidgetType
    ) -> None:
        self.sizes: Dict[str, SizeType] = {}
        self.kind = kind
        self.queries: Dict[str, List[Query]] = defaultdict(list)
        self._widgets: Dict[str, T] = {}

    @property
    def kind_name(self):
        return self.kind.value.lower()
    
    def create_widget(
        self,
        widget_name: str,
        size: SizeType
    ):
        self.sizes[widget_name] = size
    
    def add_metric(
        self,
        widget_name: str,
        query: Query
    ):
        self.queries[widget_name].append(query)