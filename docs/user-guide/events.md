# Working with Events

!!! abstract ""
    Events are at the core of `ezvent`. They represent something that has happened in your system
    and carry the necessary data related to that occurrence.

## Defining Events

In `ezvent`, events are defined as dataclasses that inherit from the `EZvent` base class:

```python
from dataclasses import dataclass
from ezvent import EZvent

@dataclass
class UserCreatedEvent(EZvent):
    user_id: int
    username: str
    email: str
```

!!! tip ""
    Events should be:
    
    - **Immutable**: Once created, an event's data should not change
    - **Self-contained**: An event should contain all the data needed to understand what happened
    - **Descriptively named**: The event name should clearly indicate what happened (e.g., `UserCreatedEvent` instead of `UserEvent`)

## Event Structure

`ezvent` events are Python dataclasses, which means they provide several benefits:

| Feature           | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| Automatic methods | Generate `__init__`, `__repr__`, and `__eq__` methods              |
| Type hints        | Support better IDE integration and static type checking            |
| Serialization     | Can be easily serialized/deserialized for storage and transmission |

The base `EZvent` class provides:

- Type registration for the event system
- Serialization/deserialization logic
- Integration with the `ezvent` framework

## Built-in Events

`ezvent` includes built-in events for system control:

### EZEndEvent

The `EZEndEvent` is used to gracefully stop the consumer after completing all in-progress events:

```python
from ezvent import publish_event
from ezvent.events import EZEndEvent

async def shutdown_consumer():
    # Stop the consumer gracefully after processing all in-progress events
    await publish_event(EZEndEvent())
```

You can specify a timeout for in-progress events:

```python
# Wait up to 30 seconds for in-progress events to complete
await publish_event(EZEndEvent(timeout=30))
```

### EZInterruptEvent

The `EZInterruptEvent` immediately stops the consumer, canceling any in-progress events:

```python
from ezvent import publish_event
from ezvent.events import EZInterruptEvent

async def emergency_shutdown():
    # Stop the consumer immediately
    await publish_event(EZInterruptEvent())
```

## Publishing Events

`ezvent` provides two ways to publish events:

=== "Single Event"

    Use `publish_event` to publish a single event:

    ```python
    from ezvent import publish_event

    async def create_user(username, email):
        user_id = 123  # In a real app, this would come from the database

        await publish_event(UserCreatedEvent(
            user_id=user_id,
            username=username,
            email=email
        ))

        return user_id
    ```

=== "Multiple Events"

    Use `publish_events` to publish multiple events at once:

    ```python
    from ezvent import publish_events

    async def bulk_create_users(users):
        user_events = []

        for username, email in users:
            user_id = hash(username) % 10000  # In a real app, this would come from the database
            user_events.append(UserCreatedEvent(
                user_id=user_id,
                username=username,
                email=email
            ))

        await publish_events(user_events)
    ```

## Event Design Best Practices

### Naming Conventions

- Use past tense for event names to indicate that something has already happened
- Be specific about what happened (e.g., `UserRegisteredEvent` instead of `UserEvent`)
- Use a consistent naming pattern throughout your application

### Data Design

!!! example ""
    ```python
    from dataclasses import dataclass, field
    from ezvent import EZvent
    from datetime import datetime
    import uuid

    @dataclass
    class UserRegisteredEvent(EZvent):
        user_id: int
        username: str
        email: str
        registration_time: datetime = field(default_factory=datetime.utcnow)
        correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
        version: str = "1.0"
    ```

??? tip "Data Design Guidelines"
    - Include all necessary data but avoid excessive information 
    - Use primitive types where possible for better serialization 
    - Include identifiers to trace the event origin 
    - Consider adding timestamps and correlation IDs for tracing 
    - Add version information if your events might evolve over time

### Event Hierarchies

You can create event hierarchies to represent related events:

```python
@dataclass
class UserEvent(EZvent):
    """Base class for all user-related events"""
    user_id: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class UserCreatedEvent(UserEvent):
    username: str
    email: str

@dataclass
class UserDeletedEvent(UserEvent):
    reason: str = None
```

### Event Evolution

As your system evolves, your events may need to change. Here are some strategies for handling event evolution:

1. **Version your events**: Include a version field in your events
2. **Make fields optional**: Use default values for new fields
3. **Create new event types**: For major changes, create new event types rather than changing existing ones

## Debugging Events

To debug events, you can:

1. Use logging in your event handlers
2. Create a specific debugging event handler that logs all events:

```python
from ezvent import on_event
import logging

logger = logging.getLogger(__name__)

@on_event
async def debug_all_events(event):
    """This handler will be called for ALL events"""
    logger.debug(f"Event received: {event.__class__.__name__} - {event}")
```

## Next Steps

Now that you understand how to create and publish events, learn about:

- [Event Handlers](handlers.md): How to process events
- [Configuration](configuration.md): How to configure the event system
