from ezq.queue_ import DEFAULT_QUEUE_NAME, get_queue


async def clean(queue_name: str = DEFAULT_QUEUE_NAME) -> None:
    pgmq = await get_queue(queue_name)
    await pgmq.purge(queue_name)
