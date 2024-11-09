import asyncio
from concurrent.futures import ThreadPoolExecutor


def handle_loop_stop(
    signame, 
    executor: ThreadPoolExecutor, 
    loop: asyncio.AbstractEventLoop,
): 
    try:
        executor.shutdown(wait=False, cancel_futures=True) 
        loop.stop()
    except Exception:
        pass

