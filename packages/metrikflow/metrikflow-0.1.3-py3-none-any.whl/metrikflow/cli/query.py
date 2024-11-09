import os

import click

from metrikflow.cli.commands import query_metric


@click.command(help='Query for Metrics via various connectors')
@click.option(
    '--metric-id',
    help='Metric ID of the metric to query for.'
)
@click.option(
    '--name',
    help='Name of the metric to query for.'
)
@click.option(
    '--kind',
    help='Kind of metric to query for (event, interval, rate, etc.).'
)
@click.option(
    '--group',
    default='default',
    help='Group of metric to query for.'
)
@click.option(
    '--newer-than',
    default='30d',
    help='Only fetch metrics newer than the specified interval.'
)
@click.option(
    '--older-than',
    help='Only fetch metrics older than the specified interval.'
)
@click.option(
    '--search',
    help='A string specified as <format>:<location/path/uri> denoting where to load existing metric from.'
)
@click.option(
    '--config',
    show_default=True,
    default=f'{os.getcwd()}/.metrikflow.json',
    help='Path to existing .metrikflow.json.'
)
@click.option(
    '--timeout',
    show_default=True,
    default=60,
    type=float,
    help='Timeout (in seconds) to send metric for storage via selected Connector format.'
)
def query(
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
    query_metric(
        metric_id=metric_id,
        name=name,
        kind=kind,
        group=group,
        newer_than=newer_than,
        older_than=older_than,
        search=search,
        config=config,
        timeout=timeout
    )

