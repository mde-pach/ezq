"""Generate API reference documentation pages for ezvent and ezq."""

import os
import pathlib


def write_markdown(filename, content):
    """Write content to a markdown file."""
    filepath = pathlib.Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)

def generate():
    """Generate the API reference documentation."""
    # Create API index page
    api_index = """# API Reference

This section provides detailed API documentation for both `ezvent` and `ezq` packages.

## Packages

- [`ezvent`](ezvent/index.md): Main event framework API
- [`ezq`](ezq/index.md): Queue implementation used by `ezvent`
"""

    write_markdown("docs/api/index.md", api_index)

    # Create ezvent API documentation
    ezvent_index = """# `ezvent` API

The `ezvent` package provides the main interface for working with events.

## Core Components

::: ezvent
    options:
        members:
            - on_event
            - publish_event
            - publish_events
            - EZvent
            - EZEndEvent
            - EZInterruptEvent
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezvent/index.md", ezvent_index)

    # Create ezq API documentation
    ezq_index = """# `ezq` API

The `ezq` package provides the queue implementation used by `ezvent`.

## Core Components

::: ezq
    options:
        members:
            - consumer
            - get_queue
            - DEFAULT_QUEUE_NAME
            - configure
            - get_config
            - EZQConfig
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezq/index.md", ezq_index)

    # Create specific reference pages for key classes
    ezvent_ezvent = """# EZvent

::: ezvent.EZvent
    options:
        show_root_heading: true
        show_source: true
        members: true
"""

    write_markdown("docs/api/ezvent/ezvent.md", ezvent_ezvent)

    ezq_config = """# EZQConfig

::: ezq.EZQConfig
    options:
        show_root_heading: true
        show_source: true
        members: true
"""

    write_markdown("docs/api/ezq/config.md", ezq_config)

    # Create reference pages for key functions
    ezvent_events = """# Event System

## Publishing Events

::: ezvent.publish_event
    options:
        show_root_heading: true
        show_source: true

::: ezvent.publish_events
    options:
        show_root_heading: true
        show_source: true

## Built-in Events

::: ezvent.EZEndEvent
    options:
        show_root_heading: true
        show_source: true

::: ezvent.EZInterruptEvent
    options:
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezvent/events.md", ezvent_events)

    ezvent_handlers = """# Event Handlers

::: ezvent.on_event
    options:
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezvent/handlers.md", ezvent_handlers)

    ezq_consumer = """# Consumer

::: ezq.consumer
    options:
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezq/consumer.md", ezq_consumer)

    ezq_queue = """# Queue Access

::: ezq.get_queue
    options:
        show_root_heading: true
        show_source: true

## Constants

::: ezq.DEFAULT_QUEUE_NAME
    options:
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezq/queue.md", ezq_queue)

    ezq_configuration = """# Configuration

::: ezq.configure
    options:
        show_root_heading: true
        show_source: true

::: ezq.get_config
    options:
        show_root_heading: true
        show_source: true
"""

    write_markdown("docs/api/ezq/configuration.md", ezq_configuration)

if __name__ == "__main__":
    generate() 