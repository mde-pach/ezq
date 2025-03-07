import logging
from typing import Optional

from async_lru import alru_cache
from tembo_pgmq_python.async_queue import PGMQueue  # type: ignore

from .config import get_config

logger = logging.getLogger(__name__)

# Re-export DEFAULT_QUEUE_NAME from config for backward compatibility
DEFAULT_QUEUE_NAME = get_config().queue.default_queue_name


@alru_cache
async def get_queue(
    queue_name: Optional[str] = None,
    *,
    host: Optional[str] = None,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
) -> PGMQueue:
    """Instanciate the PGMQ object, which is used to communicate with the PGMQ queue.
    
    Args:
        queue_name: The name of the queue to connect to (defaults to config value)
        host: The PostgreSQL host (defaults to config value)
        port: The PostgreSQL port (defaults to config value)
        username: The PostgreSQL username (defaults to config value)
        password: The PostgreSQL password (defaults to config value)
        database: The PostgreSQL database (defaults to config value)
        
    Returns:
        A PGMQueue instance connected to the PostgreSQL database
    """
    config = get_config().queue
    
    # Override defaults with function parameters if provided
    effective_host = host or config.host
    effective_port = port or config.port
    effective_username = username or config.username
    effective_password = password or config.password
    effective_database = database or config.database
    effective_queue_name = queue_name or config.default_queue_name
    
    pgmq = PGMQueue(
        host=effective_host,
        port=effective_port,
        username=effective_username,
        password=effective_password,
        database=effective_database,
    )
    try:
        await pgmq.init()
        if effective_queue_name not in await pgmq.list_queues():
            await pgmq.create_queue(effective_queue_name)
    except Exception:
        logger.exception(f"Error creating queue: {effective_queue_name}")
        raise
    return pgmq
