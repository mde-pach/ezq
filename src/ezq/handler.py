import asyncio
import logging
from functools import lru_cache
from typing import Any, Awaitable, Callable, Generic

from ezq.events import EventT, EZQEvent, EZQInternalEvent
from ezq.tasks import handle_task_errors

logger = logging.getLogger(__name__)


class _EventHandler(Generic[EventT]):
    """
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

        def _task_callback(task: asyncio.Task) -> None:
            if task.done():
                try:
                    handle_task_errors(task)
                finally:
                    _tasks.discard(task)

        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                task: asyncio.Task = asyncio.create_task(
                    asyncio.wait_for(handler(event), timeout=timeout)
                )
                task.add_done_callback(_task_callback)
                _tasks.add(task)
        elif not isinstance(event, EZQInternalEvent):
            logger.info(f"No handler registered for {event_type}")

        await asyncio.gather(*_tasks, return_exceptions=True)


@lru_cache
def get_event_handler() -> _EventHandler:
    return _EventHandler()


def on_event(
    func: Callable[[EventT], Awaitable[Any]],
) -> Callable[[EventT], Awaitable[Any]]:
    event_type = func.__annotations__.get("event")
    if not event_type or not issubclass(event_type, EZQEvent):
        raise ValueError(
            f"Event handler {func.__name__} must have a BaseEvent subclass as its first parameter"
        )

    get_event_handler().register(event_type, func)
    return func
