# `ezvent`

## Overview

`ezvent` is a Python framework for building event-driven systems with asynchronous processing capabilities. It provides a type-safe approach to event handling with a clean API.

Under the hood, ezvent uses PostgreSQL with PGMQ extension for message storage and processing.

## Key Features

- **Type-Safe Events**: Define your events using Python dataclasses for better type checking
- **Async by Design**: Built with asyncio for asynchronous event processing
- **PostgreSQL Storage**: Event persistence using PostgreSQL with PGMQ
- **Simple API**: Intuitive API for event publishing and handling
- **Configurable**: Supports configuration via environment variables or code

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL with PGMQ extension (see [pgmq](https://github.com/tembo-io/pgmq))

### Steps

```bash
pip install ezvent
```

## Quick Start

```python
import asyncio
from ezvent import EZvent, on_event, publish_event, publish_events
from ezvent.consumer import consumer  # Import consumer functionality
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

## Documentation

The framework includes documentation built with MkDocs. To view the documentation locally:

1. Install the documentation dependencies:

   ```bash
   pip install -e ".[doc]"
   ```

2. Start the documentation server:

   ```bash
   mkdocs serve
   ```

3. Open your browser and navigate to http://localhost:8000

The documentation uses several plugins for enhanced functionality:

- **api-autonav**: Automatically generates navigation for API reference
- **mkdocstrings**: Generates API documentation from docstrings
- **include-markdown**: Allows including content from other markdown files
- **awesome-pages**: Provides more control over page navigation
- **macros**: Enables variables and template-like features in markdown
- **codeinclude**: Includes code snippets from source files
- **meta-descriptions**: Generates SEO-friendly meta descriptions

To build the documentation for production:

```bash
mkdocs build
```

This will create a `site` directory with the static documentation that can be deployed to any web server.

## Configuration

ezvent can be configured through environment variables or programmatically:

### Using Environment Variables

Currently, the environment variables use the `EZQ_` prefix (this may change in future versions):

```bash
export EZQ_QUEUE_HOST=postgres.example.com
export EZQ_QUEUE_USERNAME=myuser
export EZQ_QUEUE_PASSWORD=mypassword
export EZQ_DEFAULT_QUEUE_NAME=my_app_events
```

### Programmatic Configuration

Configure ezvent directly in your code:

```python
from ezvent import configure

# Configure specific parameters
configure(
    queue_host="postgres.example.com",
    queue_username="myuser",
    queue_password="mypassword"
)
```

## Technical Details

ezvent uses PostgreSQL with PGMQ extension for message storage, providing:

- Message persistence through PostgreSQL
- Queue management with PGMQ
- Asynchronous message processing

For more details about the implementation, see the [Technical Documentation](implementation/ezq.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
