import logging
from dataclasses import asdict

from tembo_pgmq_python.async_queue import PGMQueue  # type: ignore

from ezq.events import EventMeta, EventT
from ezq.queue_ import _DEFAULT_QUEUE_NAME, get_pgmq

logger = logging.getLogger(__name__)


async def publish_event(
    event: EventT,
    *,
    queue_name: str = _DEFAULT_QUEUE_NAME,
    delay: int = 0,
    pgmq: PGMQueue | None = None,
) -> int:
    pgmq = pgmq or await get_pgmq(queue_name)

    return await pgmq.send(
        queue_name,
        {EventMeta._type_key: event.__class__.__name__, **asdict(event)},
        delay,
    )


async def publish_events(
    events: list[EventT],
    *,
    delay: int = 0,
    queue_name: str = _DEFAULT_QUEUE_NAME,
    pgmq: PGMQueue | None = None,
) -> int:
    pgmq = pgmq or await get_pgmq(queue_name)
    return await pgmq.send_batch(
        queue_name,
        [
            {EventMeta._type_key: event.__class__.__name__, **asdict(event)}
            for event in events
        ],
        delay,
    )
