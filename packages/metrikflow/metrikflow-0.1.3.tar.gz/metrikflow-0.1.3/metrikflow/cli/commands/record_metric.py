import os
import json
import datetime
from typing import (
    Literal, 
    Union, 
    Dict, 
    Any,
    List
)
from metrikflow.connectors import Connector
from metrikflow.logging.table import MetrikTable
from metrikflow.metrics import (
    MetricStore
)


def record_metric(
    name: str,
    kind: Union[
        Literal['event'],
        Literal['interval'],
        Literal['rate']
    ],
    group: str=None,
    value: float=None,
    load: str=None,
    send: str=None,
    config_path: str=None,
    timeout: Union[int, float]=60,
    tags: str=None
):
    
    if send is None:
        metric_send_location = os.path.join(
            os.getcwd(),
            f'{name}_{kind}.json'
        )

        metric_format = 'json'

    else:
        metric_format, metric_send_location = send.split(':', maxsplit=1)

    metrik_config = {}
    if os.path.exists(config_path):
        with open(config_path) as metrik_config_file:
            metrik_config = json.load(metrik_config_file)

    metrik_config['config_path'] = config_path

    store = MetricStore()
    connector = Connector()


    if load:
        load_connector_config: Dict[str, Any] = metrik_config.get('loader', {})

        metric_format, metric_load_location = load.split(':', maxsplit=1)

        metric_load_query = store.create_load_query(
            name=name,
            kind=kind,
            group=group,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=value
        )

        connector.select(
            metric_format,
            **load_connector_config
        )

        loaded_metric = connector.load(
            metric_load_location,
            metric_load_query,
            timeout=timeout
        )

        if loaded_metric:
            store.record(
                name=loaded_metric.name,
                kind=kind,
                group=loaded_metric.group,
                timestamp=loaded_metric.timestamp,
                value=loaded_metric.value
            )
    
    metric_tags: Union[
        List[
            Dict[str, str]
        ],
        None
    ] = None
    if tags:
        metric_tags = []
        tag_strings = tags.split(',')
        
        for tag_string in tag_strings:
            tag_name, tag_value = tag_string.split(':')
            metric_tags.append({
                tag_name: tag_value
            })

    metric = store.record(
        name=name,
        kind=kind,
        group=group,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        value=value,
        tags=metric_tags
    )


    send_connector_config: Dict[str, Any] = metrik_config.get(
        'sender', 
        {}
    )

    connector.select(
        metric_format,
        **send_connector_config
    )

    connector.send(
        metric_send_location,
        metric,
        timeout=timeout
    )

    table = MetrikTable([metric])

    table.generate_table()
