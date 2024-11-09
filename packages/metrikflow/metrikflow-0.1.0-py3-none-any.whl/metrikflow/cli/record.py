import os

import click

from metrikflow.cli.commands import record_metric


@click.group(help='Generate new metrics or update existing ones.')
def record():
    pass

@record.command(
    help='Record a new instance of an Event metric.'
)
@click.argument('name')
@click.argument(
    'value',
    default=1,
    type=float
)
@click.option(
    '--group',
    default='default',
    help='Group of newly created metric.'
)
@click.option(
    '--load',
    help='A string specified as <format>:<location/path/uri> denoting where to load existing metric from.'
)
@click.option(
    '--send',
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
@click.option(
    '--tags',
    help="Comma-delimited list of <key>:<value> pairs to add to a metric's tags."
)
def event(
    name: str,
    group: str,
    value: float,
    load: str,
    send: str,
    config: str,
    timeout: float,
    tags: str
):
    record_metric(
        name=name,
        kind='event',
        group=group,
        value=value,
        load=load,
        send=send,
        config_path=config,
        timeout=timeout,
        tags=tags
    )

@record.command(
    help='Record a new instance of an Interval metric.'
)
@click.argument('name')
@click.option(
    '--group',
    default='default',
    help='Group of newly created metric.'
)
@click.option(
    '--load',
    help='A string specified as <format>:<location/path/uri> denoting where to load existing metric from.'
)
@click.option(
    '--send',
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
@click.option(
    '--tags',
    help="Comma-delimited list of <key>:<value> pairs to add to a metric's tags."
)
def interval(
    name: str,
    group: str,
    load: str,
    send: str,
    config: str,
    timeout: float,
    tags: str
):
    
    record_metric(
        name=name,
        kind='interval',
        group=group,
        load=load,
        send=send,
        config_path=config,
        timeout=timeout,
        tags=tags
    )

@record.command(
    help='Record a new instance of a Rate metric.'
)
@click.argument('name')
@click.argument(
    'value', 
    default=1,
    type=float
)
@click.option(
    '--group',
    default='default',
    help='Group of newly created metric.'
)
@click.option(
    '--load',
    help='A string specified as <format>:<location/path/uri> denoting where to load existing metric from.'
)
@click.option(
    '--send',
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
@click.option(
    '--tags',
    help="Comma-delimited list of <key>:<value> pairs to add to a metric's tags."
)
def rate(
    name: str,
    group: str,
    value: float,
    load: str,
    send: str,
    config: str,
    timeout: float,
    tags: str
):
    
    record_metric(
        name=name,
        kind='rate',
        group=group,
        value=value,
        load=load,
        send=send,
        config_path=config,
        timeout=timeout,
        tags=tags
    )