import asyncio
import signal
from typing import Callable, Awaitable


def add_signal_handler(
        loop: asyncio.AbstractEventLoop,
        handler: Callable[
            ...,
            Awaitable[None]
        ],
        *args
):
    for signame in ('SIGINT', 'SIGTERM', 'SIG_IGN'):
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda signame=signame: handler(
                signame,
                *args
            )
        )