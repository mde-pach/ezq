import inspect
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from ezq.events import EZQEvent


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

    def __new__(cls, *args, **kwargs):
        new_cls = super().__new__(cls, *args, **kwargs)
        if new_cls.__name__ in EventMeta._event_types:
            raise ValueError(
                (
                    f"Duplicate event type registration: {new_cls.__name__} is already registered in file "
                    f"{inspect.getfile(EventMeta._event_types[new_cls.__name__])} and {inspect.getfile(new_cls)}"
                )
            )
        EventMeta._event_types[new_cls.__name__] = new_cls
        return new_cls
