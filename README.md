# `ezq`

## Overview

`ezq` is a powerful and easy-to-use Python library designed to abstract the complexities of event processing and consumption. It leverages asynchronous programming to provide a seamless and efficient event-driven architecture. With EZQ, developers can focus on building their applications without worrying about the underlying event management details.

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL with PGMQ extension (see [pgmq](https://github.com/tembo-io/pgmq))

### Steps

TODO

## Usage

### Quick Start

`ezq` simplifies event processing with minimal setup. Here's a quick example to get you started:

```python
import asyncio
from ezq import EZQEvent as Event, on_event, process_events, consumer
from dataclasses import dataclass

@dataclass
class MyEvent(Event):
    data: str

@on_event
async def handle_my_event(event: MyEvent):
    print("Handling event:", event.data)

async def main():
    await process_events([MyEvent(data="Hello, EZQ!")])
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

### Detailed Examples

#### Event Creation and Handling

Create a custom event by subclassing `EZQEvent` and use the `@on_event` decorator to define an event handler:

```python
from ezq.events import EZQEvent

class UserCreatedEvent(EZQEvent):
    user_id: int
    username: str

@on_event
async def handle_user_created(event: UserCreatedEvent):
    print(f"New user {event.username} created!")
```

#### Consumer Usage

The consumer continuously polls the queue for messages and dispatches them as events. You can use it as a dedicated worker in charge of getting the events from the queue and calling the appropriate handlers.

```python
import asyncio
from ezq.consumer import consumer

async def start_consumer():
    await consumer(queue_name="my_queue")

if __name__ == "__main__":
    asyncio.run(start_consumer())
```

Using the built-in `ezq` events `EZQEndEvent` and `EZQInterruptEvent`, you can programatically stop the consumer and leverage a custom behavior of you application events management.

```python
from ezq.events import EZQEndEvent, EZQInterruptEvent
from ezq import publish_event

@on_event
async def exit_consumer(event: EZQEndEvent):
    print("Exiting consumer...")


async def main():
    await publish_event(EZQEndEvent())
    await consumer()

    print("Exiting main...")


if __name__ == "__main__":
    asyncio.run(main())
```

#### EZQEndEvent

The `EZQEndEvent` event is used to stop the consumer while still waiting for the events currently processed in the event loop. The consumer will then stop fetching new events from the queue and will wait for the events currently processed to be finished.

This event is treated like any other event by the consumer, which means that the consumer will process any events before this one in the queue.

You can specify a timeout value to set a maximum waiting time before the consumer stops and cancels every events still in processing.

```python
await publish_event(EZQEndEvent(timeout=10))
```

#### EZQInterruptEvent

The `EZQInterruptEvent` event is used to stop the consumer immediately. The consumer will stop any current event processing and stop immediately.

This event is treated like any other event by the consumer, which means that the consumer will process any events before this one in the queue.

```python
await publish_event(EZQInterruptEvent())
```

#### `stop_event` parameter

The `stop_event` parameter is used to stop the consumer at any time. By using this mechanism, you can stop the consumer using a specific event for example.

```python
import asyncio
from ezq.consumer import consumer
from ezq.events import EZQEvent
from ezq import publish_event

stop_event = asyncio.Event()

class CriticalErrorEvent(EZQEvent):
    pass

@on_event
async def stop_consumer(event: CriticalErrorEvent):
    stop_event.set()

async def main():
    await publish_event(CriticalErrorEvent())
    await consumer(stop_event=stop_event)
    print("Consumer stopped")

if __name__ == "__main__":
    asyncio.run(main())
```

The `stop_event` is working differently than the `EZQEndEvent` and `EZQInterruptEvent`. The `stop_event` is not a special event, it is a parameter of the `consumer` function that is used in the internal polling loop of the consumer to know if it should stop or not.
By default, the consumer will try to wait for the already processed events to be finished before stopping.

### Key Features

TODO

## Key Concepts

### Producer

A producer is a component that creates and/or emits events into the system.

A producer captures user actions, system changes, or other triggers, and generates events that initiate the event flow throughout the system. The producer is in charge of ensuring that the event is properly serialized and sent to the event system.

### Event

An event is a message that signifies a change or action within a system.

An event represents a significant occurrence or change in state within a system. In event-driven architectures, events are the primary units of communication, triggering actions or processes. They can range from user actions, like clicking a button, to system-generated events, such as a file upload or timer expiration, or even more internal changes like a database update.

### Queue

A queue is a data structure used to temporarily store events until they are processed.

A queue is crucial for managing the flow of events, providing reliability and scalability by decoupling event production from consumption. Events are typically processed in a first-in, first-out (FIFO) order.

_Note:_ The queue is distinct from the event system. The event system is the core of the library and is responsible for the event flow, while the queue serves as the temporary storage for the events.

### Dispatcher

A dispatcher is the component that routes events to the appropriate handlers.

A dispatcher acts as the central hub in an event-driven system, responsible for routing events to the appropriate handlers. It receives events and determines which handlers should be invoked, ensuring that each event is processed by the correct component.

### Handler

A handler is a function or method designed to process specific types of events.

A handler contains the logic required to respond to an event, such as updating a database, sending a notification, or triggering another process. Handlers enable the system to dynamically react to different events.

### Listener

A listener is a component that waits for events to occur and initiates their processing.

A listener detects events and passes them to the appropriate handlers for processing, acting as the first point of contact in the event processing pipeline.

### Consumer

A consumer is a component that executes the business logic associated with events.

A consumer listens for and processes events. It subscribes to a queue or topic and performs actions based on the events it receives.
