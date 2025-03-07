import asyncio
import logging
from functools import partial
from typing import Optional

from tembo_pgmq_python.async_queue import Message, PGMQueue  # type: ignore

from ezq.dispatcher import dispatch_event  # type: ignore
from ezvent.events import EventMeta, EZEndEvent, EZInterruptEvent, EZvent

from .config import get_config
from .errors import EZQEndError, EZQInterruptError, NonExistingEventError
from .queue_ import DEFAULT_QUEUE_NAME, get_queue
from .tasks import handle_task_errors

logger = logging.getLogger(__name__)


def extract_event(message: Message) -> EZvent:
    """
    Create the appropriate event instance from a message based on the message content.
    """

    event_data = message.message
    event_type = event_data.pop(EventMeta._type_key)
    if event_type == EZEndEvent.__name__:
        return EZEndEvent()
    elif event_type == EZInterruptEvent.__name__:
        return EZInterruptEvent()
    EventClass = EventMeta._event_types.get(event_type)
    if EventClass is None:
        logger.error(f"Event type {event_type} not found")
        raise NonExistingEventError(f"Event type {event_type} not found")
    return EventClass(**event_data)


async def consumer(
    queue_name: Optional[str] = None,
    *,
    pgmq: Optional[PGMQueue] = None,
    timeout: Optional[float] = None,
    empty_poll_delay: Optional[float] = None,
    error_delay: Optional[float] = None,
    stop_event: Optional[asyncio.Event] = None,
    batch_size: Optional[int] = None,
) -> None:
    """Continuously poll a PGMQ queue for messages and dispatch them as events.

    This consumer function runs in an infinite loop (until stopped), polling the specified
    queue for messages. When a message is received, it creates an asyncio task to handle
    the event dispatch, allowing for concurrent processing of multiple events.

    Args:
        queue_name:
            The name of the PGMQ queue to consume from (defaults to configured value).
        pgmq:
            Optional pre-configured PGMQueue instance. If None, one will be created using the queue_name.
        timeout:
            Timeout in seconds for polling operations (defaults to configured value).
        empty_poll_delay:
            Time in seconds to wait before retrying when no message is found (defaults to configured value).
            Lower is faster but more CPU intensive.
        error_delay:
            Time in seconds to wait before retrying after an error (defaults to configured value).
        stop_event:
            Optional asyncio.Event that can be used to signal the consumer to stop.
        batch_size:
            Maximum number of messages to process in a single poll (defaults to configured value).
    """
    config = get_config()
    
    # Use provided values or fall back to configuration
    effective_queue_name = queue_name or config.queue.default_queue_name
    effective_timeout = timeout or config.consumer.timeout
    effective_poll_delay = empty_poll_delay or config.consumer.poll_interval
    effective_error_delay = error_delay or 0.1  # Keep the hardcoded default for now
    effective_batch_size = batch_size or config.consumer.batch_size
    
    _tasks: set[asyncio.Task] = set()
    _cleanup_tasks: set[asyncio.Task] = set()
    end_event = asyncio.Event()
    interrupt_event = asyncio.Event()

    # Initialize PGMQ if not provided
    if pgmq is None:
        pgmq = await get_queue(effective_queue_name)

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
                    asyncio.create_task(pgmq.delete(effective_queue_name, message.msg_id))
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
                    effective_queue_name, vt=effective_timeout + effective_error_delay, batch_size=effective_batch_size
                )
                # message = await pgmq.read(effective_queue_name, vt=effective_timeout + effective_error_delay)
                logger.debug(f"Messages received: {messages}")
                if messages is None:
                    await asyncio.sleep(effective_poll_delay)
                    continue
            except ConnectionError as e:
                logger.error(f"Connection error: {e}, retrying...")
                await asyncio.sleep(effective_error_delay)
                continue
            except Exception as e:
                logger.error(f"Unexpected error while listening to queue: {e}")
                await asyncio.sleep(effective_error_delay)
                continue

        for message in messages:
            logger.debug(f"Message received: {message}")
            try:
                event = extract_event(message)
            except NonExistingEventError as e:
                logger.exception(e)
                continue

            try:
                if isinstance(event, EZEndEvent):
                    end_event.set()
                if isinstance(event, EZInterruptEvent):
                    interrupt_event.set()
                task = asyncio.create_task(dispatch_event(event, timeout=effective_timeout))
                _tasks.add(task)
                task.add_done_callback(partial(_task_callback, message))
            except Exception as e:
                logger.error(f"Unexpected error while dispatching event: {e}")

    logger.debug("Consumer exiting")
    if _tasks:
        await asyncio.gather(*_tasks, return_exceptions=True)
    if _cleanup_tasks:
        await asyncio.gather(*_cleanup_tasks)
