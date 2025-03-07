# Quick Start Guide

This guide will help you quickly get started with `ezvent` by building a simple event-driven application.

## Core Concepts

!!! info ""
    Before diving in, let's understand some basic concepts:

    - **Events**: Objects that represent something that happened in your system
    - **Event Handlers**: Functions that process events when they occur
    - **Consumer**: A process that listens for events and dispatches them to handlers
    - **Queue**: A storage mechanism that holds events until they are processed

## Minimal Example

Here's a simple example that demonstrates the core functionality of `ezvent`:

```python
import asyncio
from ezvent import EZvent, on_event, publish_events, publish_event
from ezvent.consumer import consumer
from dataclasses import dataclass

# 1. Define your event
@dataclass
class MyEvent(EZvent):
    data: str

# 2. Define an event handler
@on_event
async def handle_my_event(event: MyEvent):
    print("Handling event:", event.data)

# 3. Main function to process events and run the consumer
async def main():
    # Publish an event
    await publish_events([MyEvent(data="Hello, ezvent!")])
    # Start the consumer to process events
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

## Step-by-Step Tutorial

### 1. Define Your Events

Events in `ezvent` are Python dataclasses that inherit from `EZvent`:

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
    Events should be immutable, self-contained, and descriptively named to clearly indicate what happened.

### 2. Create Event Handlers

Handlers process events when they occur. Use the `@on_event` decorator to register a handler:

```python
from ezvent import on_event

@on_event
async def send_welcome_email(event: UserCreatedEvent):
    print(f"Sending welcome email to {event.email}")

@on_event
async def notify_admin(event: UserCreatedEvent):
    print(f"New user created: {event.username} (ID: {event.user_id})")
```

!!! note ""
    You can have multiple handlers for the same event type, and they will all be called when the event is processed.

### 3. Publish Events

`ezvent` provides two methods for publishing events:

=== "Single Event"

    ```python
    from ezvent import publish_event

    async def create_user(username, email):
        user_id = hash(username) % 10000
        await publish_event(UserCreatedEvent(
            user_id=user_id,
            username=username,
            email=email
        ))
        return user_id
    ```

=== "Multiple Events"

    ```python
    from ezvent import publish_events

    async def bulk_create_users(users):
        user_events = []
        for username, email in users:
            user_id = hash(username) % 10000
            user_events.append(UserCreatedEvent(
                user_id=user_id,
                username=username,
                email=email
            ))
        await publish_events(user_events)
    ```

### 4. Run the Consumer

The consumer processes events from the queue and dispatches them to handlers:

```python
from ezvent.consumer import consumer
import asyncio

async def main():
    # Run the consumer
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

!!! warning ""
    In production applications, you would typically run the consumer in a separate process or as a background task.

## Complete Example

Here's a more comprehensive example that demonstrates a user registration system:

??? example "User Registration System"
    ```python
    import asyncio
    from dataclasses import dataclass
    from ezvent import EZvent, on_event, publish_event, publish_events
    from ezvent.consumer import consumer

    # Events
    @dataclass
    class UserCreatedEvent(EZvent):
        user_id: int
        username: str
        email: str

    @dataclass
    class WelcomeEmailSentEvent(EZvent):
        user_id: int
        email: str

    # Handlers
    @on_event
    async def send_welcome_email(event: UserCreatedEvent):
        print(f"Sending welcome email to {event.email}")
        # In a real app, you would actually send an email here

        # Publish a follow-up event
        await publish_event(WelcomeEmailSentEvent(
            user_id=event.user_id,
            email=event.email
        ))

    @on_event
    async def notify_admin(event: UserCreatedEvent):
        print(f"Admin notification: New user {event.username} created")

    @on_event
    async def log_email_sent(event: WelcomeEmailSentEvent):
        print(f"Email sent to user {event.user_id} at {event.email}")

    # Business logic
    async def register_user(username, email):
        # In a real app, you would save to a database
        user_id = hash(username) % 10000

        # Publish an event
        await publish_event(UserCreatedEvent(
            user_id=user_id,
            username=username,
            email=email
        ))

        return user_id

    # Main function
    async def main():
        # Register some users
        await register_user("alice", "alice@example.com")
        await register_user("bob", "bob@example.com")

        # Run the consumer to process events
        # In production, this would typically run as a separate process
        print("Starting consumer to process events...")
        await consumer()

    if __name__ == "__main__":
        asyncio.run(main())
    ```

## Next Steps

Now that you've seen the basics, check out:

- [Events Guide](../user-guide/events.md): Learn more about creating and working with events
- [Handler Guide](../user-guide/handlers.md): Learn more about event handlers
- [Configuration](../user-guide/configuration.md): Learn about configuring `ezvent`
