import logging

from async_lru import alru_cache
from tembo_pgmq_python.async_queue import PGMQueue  # type: ignore

logger = logging.getLogger(__name__)

DEFAULT_QUEUE_NAME = "ezq"


@alru_cache
async def get_queue(
    queue_name: str,
    *,
    host: str = "localhost",
    port: int = 5432,
    username: str = "postgres",
    password: str = "postgres",
    database: str = "postgres",
) -> PGMQueue:
    """Instanciate the PGMQ object, which is used to communicate with the PGMQ queue."""
    pgmq = PGMQueue(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
    )
    try:
        await pgmq.init()
        if queue_name not in await pgmq.list_queues():
            await pgmq.create_queue(queue_name)
    except Exception:
        logger.exception("Error creating queue")
        raise
    return pgmq
