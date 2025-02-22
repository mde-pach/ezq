from typing import Any, ClassVar, TypeVar, dataclass_transform

from attrs import define


# TODO: WIP
@define(frozen=True)
class Config:
    """
    EZQ configuration for the event class.
    """


# TODO: WIP
@define()
class Meta:
    """
    EZQ meta informations of the event instance.
    """


@dataclass_transform()
class EventMeta(type):
    """
    EventMeta is a metaclass that provides automatic registration of event types.

    When a new class inherits from BaseEvent, this metaclass:
    1. Stores the class in _event_types dictionary using the class name as key
    2. Uses _type_key value as the key to store/retrieve event type names in messages

    This enables automatic serialization/deserialization of events when:
    - Sending events: The event type name is added to the message
    - Receiving events: The event type name is used to reconstruct the correct event class
    """

    _event_types: ClassVar[dict[str, type["EZQEvent"]]] = {}
    _type_key: ClassVar[str] = "_type"

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
        **kwargs,
    ):
        annotations: dict[str, Any] = dct.get("__annotations__", {})
        for base in bases:
            if hasattr(base, "__annotations__"):
                annotations.update(base.__annotations__)
        dct["__annotations__"] = annotations

        new_cls = define(
            frozen=True,
            kw_only=True,
            slots=False,
            auto_detect=True,
        )(super().__new__(cls, name, bases, dct, **kwargs))
        setattr(new_cls, cls._type_key, new_cls.__name__)
        if new_cls.__name__ in EventMeta._event_types:
            # TODO: handle that as attrs dataclass seems to duplicate the original class declaration
            pass
            # print(EventMeta._event_types[new_cls.__name__], "already declared")
            # raise ValueError(
            #     (
            #         f"Duplicate event type registration: {new_cls.__name__} is already registered in file "
            #         f"{inspect.getfile(EventMeta._event_types[new_cls.__name__])} and {inspect.getfile(new_cls)}"
            #     )
            # )
        EventMeta._event_types[new_cls.__name__] = new_cls  # type: ignore
        return new_cls


# @define(kw_only=True, auto_detect=True, auto_attribs=True)
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

    _type: ClassVar[str]


class EZQInternalEvent(EZQEvent):
    pass


class EZQInterruptEvent(EZQInternalEvent):
    pass


class EZQEndEvent(EZQInternalEvent):
    timeout: float = 10.0


EventT = TypeVar("EventT", bound=EZQEvent)
