# EZQ Library

## Overview

EZQ is a powerful and easy-to-use Python library designed to abstract the complexities of event processing and consumption. It leverages asynchronous programming to provide a seamless and efficient event-driven architecture. With EZQ, developers can focus on building their applications without worrying about the underlying event management details.

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL with PGMQ extension (see [pgmq](https://github.com/tembo-io/pgmq))

### Steps

TODO

## Usage

### Quick Start

EZQ simplifies event processing with minimal setup. Here's a quick example to get you started:

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
    await asyncio.gather(consumer())

if __name__ == "__main__":
    asyncio.run(main())
```

### Key Features

TODO

## Concepts

### Asynchronous Programming

EZQ leverages Python's `asyncio` library to perform non-blocking I/O operations, enabling concurrent event processing without the need for complex threading models. To use the full power of EZQ, you should use async functions and asynchronous I/O operation through `asyncio` based implementations (e.g. [`aiohttp`](https://github.com/aio-libs/aiohttp), [`aiopg`](https://github.com/aio-libs/aiopg/), etc...)

EZQ is totally thread-safe and ensure that an event will always be processed once and only once.

### Event-Driven Architecture

EZQ's architecture is fundamentally built around the concept of events, which are the primary units of communication and processing within the system. By defining events as data classes, EZQ allows developers to create structured, type-safe events that can be easily serialized and deserialized. This design choice ensures that events are both scalable and maintainable, enabling systems to respond to changes in real-time.

#### Key Features and Problem Solving

1. **Decoupling of Event Production and Consumption**:

   - EZQ decouples the production of events from their consumption. This means that the components responsible for generating events do not need to know about the components that will handle them. This separation of concerns leads to more modular and flexible system architectures.

2. **Automatic Event Registration**:

   - EZQ simplifies the process of adding new event types to the system, as developers do not need to manually register each event type. It also ensures that events are correctly serialized and deserialized, reducing the potential for errors.

3. **Flexible Event Dispatching**:

   - EZQ enables multiple handlers to be registered for a single event type. This flexibility allows for complex event processing workflows, where different parts of the system can react to the same event in different ways.

4. **Robust Error Handling**:
   - EZQ includes mechanisms for handling errors that may occur during event processing, such as task timeouts or connection issues. This ensures that the system can continue to operate smoothly even in the face of unexpected problems.

### Queue System

EZQ implements [pgmq](https://github.com/tembo-io/pgmq) under the hood to manage event flow.

## License

This project is licensed under the MIT License.
