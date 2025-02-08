from dataclasses import dataclass
from typing import ClassVar, TypeVar

from ezq.base import EventMeta


@dataclass(frozen=True)
class Config:
    pass


@dataclass()
class Meta:
    pass


@dataclass
class EZQEvent(metaclass=EventMeta):
    """
    Base class for all events in the system.

    All event classes should inherit from this class to enable automatic registration
    and handling through the event system.

    Example:
        >>> class UserCreatedEvent(BaseEvent):
        ...     user_id: int
        ...     username: str
        ...
        >>> event = UserCreatedEvent(user_id=1, username="john")
        >>> await process_event(event)  # Send event to queue

        >>> @on_event
        ... async def handle_user_created(event: UserCreatedEvent):
        ...     print(f"New user {event.username} created!")
        ...
        >>> await listener()  # Will process events and call handlers
    """

    # config: ClassVar[Config] = Config()
    # meta: ClassVar[Meta] = Meta()


class EZQInternalEvent(EZQEvent):
    pass


class EZQInterruptEvent(EZQInternalEvent):
    pass


class EZQEndEvent(EZQInternalEvent):
    timeout: float


EventT = TypeVar("EventT", bound=EZQEvent)
