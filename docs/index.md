# EZQ: Easy Event Queue

<div class="hero-banner">
    <p class="hero-subtitle">A powerful and easy-to-use Python library for event processing</p>
</div>

EZQ is a Python library designed to abstract the complexities of event processing and consumption. It leverages asynchronous programming to provide a seamless and efficient event-driven architecture. With EZQ, developers can focus on building their applications without worrying about the underlying event management details.

## Features

- **Type-Safe Events**: Define your events using Python dataclasses for better type checking
- **Async by Design**: Built from the ground up with asyncio support
- **Postgres Backend**: Reliable message storage using PostgreSQL with PGMQ
- **Simple API**: Clean, intuitive API that hides complexity
- **Flexible Configuration**: Easy configuration through environment variables or code
- **Pluggable Architecture**: Extensible design that can adapt to your needs

## Quick Start

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

## Installation

```bash
pip install ezq
```

## Why EZQ?

EZQ was built to simplify event-driven architectures while maintaining the power and flexibility needed for production systems. By leveraging PostgreSQL with the PGMQ extension, EZQ provides a reliable and scalable event queue that can handle millions of events with ease.

## Documentation

- [Getting Started](getting-started/installation.md): Installation and first steps
- [User Guide](user-guide/events.md): Comprehensive guide to EZQ features
- [API Reference](autoapi/ezq/index.md): Detailed API documentation
- [Configuration](user-guide/configuration.md): Configuration guide

## License

EZQ is released under the MIT License. See the LICENSE file for more details.
