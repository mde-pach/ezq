from src.ezq.queue_ import _DEFAULT_QUEUE_NAME, get_pgmq


async def clean(queue_name: str = _DEFAULT_QUEUE_NAME) -> None:
    pgmq = await get_pgmq(queue_name)
    await pgmq.purge(queue_name)
