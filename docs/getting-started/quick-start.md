# Quick Start

This guide will help you quickly get started with EZQ by building a simple event-driven application.

## Basic Concepts

Before diving in, let's understand some basic concepts:

- **Events**: Objects that represent something that happened in your system
- **Event Handlers**: Functions that process events when they occur
- **Consumer**: A process that listens for events and dispatches them to handlers
- **Queue**: A storage mechanism that holds events until they are processed

## Simple Example

Here's a minimal example that demonstrates the core functionality of EZQ:

```python
import asyncio
from ezq import EZQEvent as Event, on_event, process_events, consumer
from dataclasses import dataclass

# 1. Define your event
@dataclass
class MyEvent(Event):
    data: str

# 2. Define an event handler
@on_event
async def handle_my_event(event: MyEvent):
    print("Handling event:", event.data)

# 3. Main function to process events and run the consumer
async def main():
    # Publish an event
    await process_events([MyEvent(data="Hello, EZQ!")])
    # Start the consumer to process events
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

## Step-by-Step Explanation

### 1. Define Your Event

Events in EZQ are dataclasses that inherit from `EZQEvent`:

```python
from dataclasses import dataclass
from ezq import EZQEvent as Event

@dataclass
class UserCreatedEvent(Event):
    user_id: int
    username: str
    email: str
```

Events can contain any data you need to represent what happened.

### 2. Create Event Handlers

Handlers process events when they occur. Use the `@on_event` decorator to register a handler:

```python
from ezq import on_event

@on_event
async def send_welcome_email(event: UserCreatedEvent):
    print(f"Sending welcome email to {event.email}")

@on_event
async def notify_admin(event: UserCreatedEvent):
    print(f"New user created: {event.username} (ID: {event.user_id})")
```

You can have multiple handlers for the same event type, and they will all be called when the event is processed.

### 3. Publish Events

Use `process_events` to publish events to the queue:

```python
from ezq import process_events

async def create_user(username, email):
    # Create user in database
    user_id = 123  # In a real app, this would come from the database

    # Publish event
    await process_events([
        UserCreatedEvent(
            user_id=user_id,
            username=username,
            email=email
        )
    ])

    return user_id
```

### 4. Run the Consumer

The consumer processes events from the queue and dispatches them to handlers:

```python
from ezq import consumer
import asyncio

async def main():
    # Run the consumer
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

You typically run the consumer in a separate process or as a background task.

## Complete Example

Here's a more complete example that demonstrates a user registration system:

```python
import asyncio
from dataclasses import dataclass
from ezq import EZQEvent as Event, on_event, process_events, consumer, publish_event

# Events
@dataclass
class UserCreatedEvent(Event):
    user_id: int
    username: str
    email: str

@dataclass
class WelcomeEmailSentEvent(Event):
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

- [Event Guide](../user-guide/events.md): Learn more about creating and working with events
- [Handler Guide](../user-guide/handlers.md): Learn more about event handlers
- [Configuration](../user-guide/configuration.md): Learn about configuring EZQ
