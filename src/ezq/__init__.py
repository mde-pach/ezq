from .config import EZQConfig, configure, get_config
from .consumer import consumer
from .queue_ import DEFAULT_QUEUE_NAME, get_queue

__all__ = [
    "consumer",
    "get_queue",
    "DEFAULT_QUEUE_NAME",
    "configure",
    "get_config",
    "EZQConfig",
]
