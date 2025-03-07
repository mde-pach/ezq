# `ezvent`: Event-Driven Framework

<div class="hero-banner">
    <p class="hero-subtitle">A Python framework for building event-driven systems</p>
</div>

!!! abstract ""
    `ezvent` is a Python framework for implementing event-driven architectures. It provides type-safe
    event definitions and handlers with asyncio support, using PostgreSQL for message storage through
    the PGMQ extension.

## ✨ Features

- **Type-Safe Events**: Define events using Python dataclasses
- **Async by Design**: Built with asyncio for asynchronous processing
- **PostgreSQL Storage**: Message persistence using PostgreSQL/PGMQ
- **Simple API**: Easy-to-use API for publishing and handling events

## 🚀 Quick Start

```python
import asyncio
from ezvent import EZvent, on_event, publish_event, publish_events
from ezvent.consumer import consumer
from dataclasses import dataclass

@dataclass
class MyEvent(EZvent):
    data: str

@on_event
async def handle_my_event(event: MyEvent):
    print("Handling event:", event.data)

async def publish_example():
    # Publish a single event
    await publish_event(MyEvent(data="Hello, ezvent!"))

    # Or publish multiple events
    await publish_events([
        MyEvent(data="First event"),
        MyEvent(data="Second event")
    ])

async def consume_events():
    # Start the consumer to process events
    await consumer()

if __name__ == "__main__":
    asyncio.run(publish_example())
    # In a real application, you would typically run the consumer in a separate process
    # asyncio.run(consume_events())
```

## 📦 Installation

```bash
pip install ezvent
```

!!! tip ""
    For development, you can install in editable mode with documentation dependencies:
    ```bash
    pip install -e ".[doc]"
    ```

## 📚 Documentation Sections

- [Getting Started](getting-started/installation.md): Installation and basic setup
- [User Guide](user-guide/events.md): Guide to using `ezvent`
- [Technical Details](implementation/ezq.md): Implementation details of the `ezq` message queue
- [API Reference](api/index.md): API documentation
- [Configuration](user-guide/configuration.md): Configuration options

## 📄 License

`ezvent` is released under the MIT License. See the LICENSE file for more details.
