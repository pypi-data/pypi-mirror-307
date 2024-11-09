import os
import json
import datetime
from typing import (
    Literal, 
    Union, 
    Dict, 
    Any
)
from metrik.connectors import Connector
from metrik.logging.table import MetrikTable
from metrik.metrics import (
    MetricStore
)


def query_metric(
    metric_id: str,
    name: str,
    kind: str,
    group: str,
    newer_than: str,
    older_than: str,
    search: str,
    config: str,
    timeout: float
):
    pass
