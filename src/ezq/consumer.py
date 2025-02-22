import asyncio
import logging
from functools import partial
from typing import Optional

from tembo_pgmq_python.async_queue import Message, PGMQueue  # type: ignore

from .errors import EZQEndError, EZQInterruptError, NonExistingEventError
from .events import EventMeta, EZQEndEvent, EZQEvent, EZQInterruptEvent
from .handler import get_event_handler
from .queue_ import DEFAULT_QUEUE_NAME, get_queue
from .tasks import handle_task_errors

logger = logging.getLogger(__name__)


def extract_event(message: Message) -> EZQEvent:
    """
    Create the appropriate event instance from a message based on the message content.
    """

    event_data = message.message
    event_type = event_data.pop(EventMeta._type_key)
    if event_type == EZQEndEvent.__name__:
        return EZQEndEvent()
    elif event_type == EZQInterruptEvent.__name__:
        return EZQInterruptEvent()
    EventClass = EventMeta._event_types.get(event_type)
    if EventClass is None:
        logger.error(f"Event type {event_type} not found")
        raise NonExistingEventError(f"Event type {event_type} not found")
    return EventClass(**event_data)


async def consumer(
    queue_name: str = DEFAULT_QUEUE_NAME,
    *,
    pgmq: PGMQueue | None = None,
    timeout: float = 1,
    empty_poll_delay: float = 0.01,
    error_delay: float = 0.1,
    stop_event: Optional[asyncio.Event] = None,
    batch_size: int = 100,
) -> None:
    """Continuously poll a PGMQ queue for messages and dispatch them as events.

    This consumer function runs in an infinite loop (until stopped), polling the specified
    queue for messages. When a message is received, it creates an asyncio task to handle
    the event dispatch, allowing for concurrent processing of multiple events.

    Args:
        queue_name:
            The name of the PGMQ queue to consume from.
        pgmq:
            Optional pre-configured PGMQueue instance. If None, one will be created using the queue_name.
        empty_poll_delay:
            Time in seconds to wait before retrying when no message is found.
            Lower is faster but more CPU intensive.
        error_delay:
            Time in seconds to wait before retrying after encountering an error.
            Lower is faster but can result in tight error loops.
        stop_event:
            Optional asyncio.Event that can be used to gracefully stop the consumer.
            When set, the consumer will finish processing current tasks and exit.

    There are 3 ways to stop the consumer:
        stop_event:
            Using the asyncio.Event mechanism, you can stop the consumer by setting the event.
            This is useful if you want to stop the consumer from another thread.
        EZQEndEvent:
            This event is used to stop the consumer when the queue is empty.
        EZQInterruptEvent:
            This event is used to stop the consumer immediately.
    """
    _tasks: set[asyncio.Task] = set()
    _cleanup_tasks: set[asyncio.Task] = set()
    end_event = asyncio.Event()
    interrupt_event = asyncio.Event()

    pgmq = pgmq or await get_queue(queue_name)

    def _task_callback(message: Message, task: asyncio.Task) -> None:
        if task.done():
            try:
                handle_task_errors(task)
            except EZQEndError:
                end_event.set()
            except EZQInterruptError:
                interrupt_event.set()
            except Exception:
                pass
            else:
                _cleanup_tasks.add(
                    asyncio.create_task(pgmq.delete(queue_name, message.msg_id))
                )
            finally:
                _tasks.discard(task)
        else:
            logger.error(f"Task {task} is not done, this should not happen")

    while not (stop_event and stop_event.is_set()) and not end_event.is_set():
        if interrupt_event.is_set():
            raise EZQInterruptError()
        if not end_event.is_set():
            try:
                messages = await pgmq.read_batch(
                    queue_name, vt=timeout + error_delay, batch_size=batch_size
                )
                # message = await pgmq.read(queue_name, vt=timeout + error_delay)
                logger.debug(f"Messages received: {messages}")
                if messages is None:
                    await asyncio.sleep(empty_poll_delay)
                    continue
            except ConnectionError as e:
                logger.error(f"Connection error: {e}, retrying...")
                await asyncio.sleep(error_delay)
                continue
            except Exception as e:
                logger.error(f"Unexpected error while listening to queue: {e}")
                await asyncio.sleep(error_delay)
                continue

        for message in messages:
            logger.debug(f"Message received: {message}")
            try:
                event = extract_event(message)
            except NonExistingEventError as e:
                logger.exception(e)
                continue

            try:
                if isinstance(event, EZQEndEvent):
                    end_event.set()
                if isinstance(event, EZQInterruptEvent):
                    interrupt_event.set()
                task = asyncio.create_task(dispatch_event(event, timeout=timeout))
                _tasks.add(task)
                task.add_done_callback(partial(_task_callback, message))
            except Exception as e:
                logger.error(f"Unexpected error while dispatching event: {e}")

    logger.debug("Consumer exiting")
    if _tasks:
        await asyncio.gather(*_tasks, return_exceptions=True)
    if _cleanup_tasks:
        await asyncio.gather(*_cleanup_tasks)


async def dispatch_event(event: EZQEvent, *, timeout: float) -> None:
    await get_event_handler().handle_event(event, timeout=timeout)
