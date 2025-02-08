import asyncio
import logging
from functools import lru_cache
from typing import Any, Awaitable, Callable, Coroutine, Generic, Optional

from tembo_pgmq_python.async_queue import Message, PGMQueue  # type: ignore

from ezq.base import EventMeta
from ezq.events import (
    EventT,
    EZQEndEvent,
    EZQEvent,
    EZQInternalEvent,
    EZQInterruptEvent,
)
from ezq.queue_ import _DEFAULT_QUEUE_NAME, get_pgmq

logger = logging.getLogger(__name__)


def extract_event(message: Message) -> EZQEvent:
    event_data = message.message
    event_type = event_data.pop(EventMeta._type_key)
    if event_type == EZQEndEvent.__name__:
        return EZQEndEvent()
    elif event_type == EZQInterruptEvent.__name__:
        return EZQInterruptEvent()
    EventClass = EventMeta._event_types.get(event_type)
    if EventClass is None:
        raise ValueError(f"Event type {event_type} not found")
    return EventClass(**event_data)


def _handle_task_errors(result: BaseException | None) -> None:
    """Handle and log any errors from an asyncio task."""
    match result:
        case None:
            return
        case EZQEndError():
            raise EZQEndError(result) from None
        case EZQInterruptError():
            raise EZQInterruptError(result) from None
        case TimeoutError():
            logger.warning(f"Task timed out: {result}")
        case asyncio.CancelledError():
            logger.warning(f"Task cancelled: {result}")
        case Exception():
            raise result


async def consumer(
    queue_name: str = _DEFAULT_QUEUE_NAME,
    *,
    pgmq: PGMQueue | None = None,
    timeout: float = 1,
    empty_poll_delay: float = 0.01,
    error_delay: float = 0.1,
    stop_event: Optional[asyncio.Event] = None,
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
    end_event = asyncio.Event()
    interrupt_event = asyncio.Event()

    def _discard_task(
        task: asyncio.Task, success_callback: Callable[[], Coroutine[Any, Any, Any]]
    ) -> None:
        if task.done():
            try:
                _handle_task_errors(task.exception())
            except EZQEndError:
                end_event.set()
            except EZQInterruptError:
                interrupt_event.set()
            except Exception:
                pass
            else:
                asyncio.create_task(success_callback())
            finally:
                _tasks.discard(task)

    pgmq = pgmq or await get_pgmq(queue_name)

    while not (stop_event and stop_event.is_set()) and not end_event.is_set():
        if interrupt_event.is_set():
            raise EZQInterruptError()
        if not end_event.is_set():
            try:
                message = await pgmq.read(queue_name, vt=timeout + error_delay)
                if message is None:
                    await asyncio.sleep(empty_poll_delay)
                    continue
                event = extract_event(message)
            except ConnectionError as e:
                logger.error(f"Connection error: {e}, retrying...")
                await asyncio.sleep(error_delay)
                continue
            except Exception as e:
                logger.error(f"Unexpected error while listening to queue: {e}")
                await asyncio.sleep(error_delay)
                continue

            logger.debug(f"Message received: {message}")
            try:
                if isinstance(event, EZQEndEvent):
                    end_event.set()
                if isinstance(event, EZQInterruptEvent):
                    interrupt_event.set()
                task = asyncio.create_task(dispatch_event(event, timeout=timeout))
                _tasks.add(task)
                task.add_done_callback(
                    lambda _: _discard_task(
                        task,
                        lambda: pgmq.delete(queue_name, message.msg_id),
                    )
                )
            except Exception as e:
                logger.error(f"Unexpected error while dispatching event: {e}")

    logger.debug("Consumer exiting")
    if _tasks:
        await asyncio.gather(*_tasks, return_exceptions=True)


async def dispatch_event(event: EZQEvent, *, timeout: float) -> None:
    await get_event_handler().handle_event(event, timeout=timeout)


def on_event(
    func: Callable[[EventT], Awaitable[Any]],
) -> Callable[[EventT], Awaitable[Any]]:
    event_type = func.__annotations__.get("event")
    if not event_type or not issubclass(event_type, EZQEvent):
        raise ValueError(
            f"Event handler {func.__name__} must have a BaseEvent subclass as its first parameter"
        )

    get_event_handler().register(event_type, func)  # type: ignore
    return func


class EZQError(Exception):
    pass


class EZQEndError(EZQError):
    pass


class EZQInterruptError(EZQError):
    pass


class _EventHandler(Generic[EventT]):
    """
    Overview:
        The _EventHandler class is a generic, asynchronous event dispatcher designed to manage and execute
        event handlers registered for specific event types. It plays a central role in the ezq architecture
        by decoupling event production from event consumption.

        This design enables multiple event handlers to be registered for a single event type, all of which
        are invoked concurrently using asyncio's asynchronous capabilities.

    Usage:
        >>> # Define a custom event by subclassing a common event base (e.g., BaseEvent)
        ... class UserRegisteredEvent(BaseEvent):
        ...     email: str

        >>> # Register an asynchronous event handler using the provided on_event decorator
        ... @on_event
        ... async def welcome_email_handler(event: UserRegisteredEvent):
        ...     print(f"Sending welcome email to {event.email}")

        >>> # Retrieve the singleton event handler instance and dispatch the event
        >>> event_handler = get_event_handler()
        >>> user_event = UserRegisteredEvent(email="user@example.com")
        >>> await event_handler.handle_event(user_event)
    """

    _handlers: dict[type[EventT], list[Callable[[EventT], Awaitable[Any]]]]

    def __init__(self) -> None:
        self._handlers = {}

    def register(
        self,
        event_type: type[EventT],
        handler: Callable[[EventT], Awaitable[Any]],
    ) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def handle_event(self, event: EventT, *, timeout: float) -> None:
        _tasks: set[asyncio.Task] = set()

        def _discard_task(task: asyncio.Task) -> None:
            if task.done():
                try:
                    _handle_task_errors(task.exception())
                except EZQInterruptError:
                    raise
                finally:
                    _tasks.discard(task)

        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                task: asyncio.Task = asyncio.create_task(
                    asyncio.wait_for(handler(event), timeout=timeout)
                )
                task.add_done_callback(_discard_task)
                _tasks.add(task)
        elif not isinstance(event, EZQInternalEvent):
            logger.info(f"No handler registered for {event_type}")

        for result in await asyncio.gather(*_tasks, return_exceptions=True):
            match result:
                case EZQEndError():
                    raise EZQEndError(result) from None
                case EZQInterruptError():
                    raise EZQInterruptError(result) from None
                case Exception():
                    logger.exception(
                        f"Error while handling event {event}", exc_info=result
                    )


@lru_cache
def get_event_handler() -> _EventHandler:
    return _EventHandler()
