# Configuration Guide

!!! abstract ""
    `ezvent` provides a flexible configuration system that allows you to customize its behavior
    according to your needs. This guide explains how to configure `ezvent` for different environments.

## Configuration Methods

There are two primary ways to configure `ezvent`:

=== "Environment Variables"
    Set environment variables with the `EZQ_` prefix (current implementation, may change in future versions)

    ```bash
    export EZQ_QUEUE_HOST=postgres.example.com
    export EZQ_QUEUE_PORT=5432
    ```

=== "Programmatic Configuration"
    Configure options directly in your code

    ```python
    from ezvent import configure

    configure(
        queue_host="postgres.example.com",
        queue_port=5432
    )
    ```

!!! info ""
    When determining the value for a configuration option, `ezvent` follows this precedence order:

    1. Programmatic configuration (highest priority)
    2. Environment variables
    3. Default values (lowest priority)

    This means that if you set a value programmatically, it will override any environment variable or default value.

## Environment Variables

Environment variables are excellent for configuring `ezvent` in production environments. All configuration options can be set using environment variables with the `EZQ_` prefix.

!!! note ""
    The `EZQ_` prefix is from the underlying `ezq` implementation and may change in future versions.

```bash
# Database connection
export EZQ_QUEUE_HOST=postgres.example.com
export EZQ_QUEUE_PORT=5432
export EZQ_QUEUE_USERNAME=app_user
export EZQ_QUEUE_PASSWORD=secure_password
export EZQ_QUEUE_DATABASE=events_db
export EZQ_DEFAULT_QUEUE_NAME=my_app_events

# Consumer settings
export EZQ_CONSUMER_POLL_INTERVAL=0.5
export EZQ_CONSUMER_BATCH_SIZE=20
export EZQ_CONSUMER_CONCURRENT_HANDLERS=10
```

## Programmatic Configuration

You can also configure `ezvent` directly in your code:

```python
from ezvent import configure

# Configure with specific parameters
configure(
    queue_host="postgres.example.com",
    queue_port=5432,
    queue_username="app_user",
    queue_password="secure_password",
    queue_database="events_db",
    default_queue_name="my_app_events",

    consumer_poll_interval=0.5,
    consumer_batch_size=20,
    consumer_concurrent_handlers=10
)
```

This is useful for development environments or when you need to set configuration options dynamically based on other factors.

## Configuration Options

### Queue Configuration

Configuration options for the message queue connection:

| Parameter                | Environment Variable               | Default   | Description                         |
| ------------------------ | ---------------------------------- | --------- | ----------------------------------- |
| `host`                   | `EZQ_QUEUE_HOST`                   | localhost | PostgreSQL host                     |
| `port`                   | `EZQ_QUEUE_PORT`                   | 5432      | PostgreSQL port                     |
| `username`               | `EZQ_QUEUE_USERNAME`               | postgres  | PostgreSQL username                 |
| `password`               | `EZQ_QUEUE_PASSWORD`               | postgres  | PostgreSQL password                 |
| `database`               | `EZQ_QUEUE_DATABASE`               | postgres  | PostgreSQL database                 |
| `default_queue_name`     | `EZQ_DEFAULT_QUEUE_NAME`           | ezq       | Default queue name                  |
| `connection_timeout`     | `EZQ_QUEUE_CONNECTION_TIMEOUT`     | 10        | Connection timeout in seconds       |
| `connection_retries`     | `EZQ_QUEUE_CONNECTION_RETRIES`     | 3         | Number of connection retry attempts |
| `connection_retry_delay` | `EZQ_QUEUE_CONNECTION_RETRY_DELAY` | 1         | Delay between retries in seconds    |

### Consumer Configuration

Configuration options for the event consumer:

| Parameter               | Environment Variable                 | Default | Description                                    |
| ----------------------- | ------------------------------------ | ------- | ---------------------------------------------- |
| `poll_interval`         | `EZQ_CONSUMER_POLL_INTERVAL`         | 1.0     | Time in seconds between empty polls            |
| `batch_size`            | `EZQ_CONSUMER_BATCH_SIZE`            | 10      | Maximum number of messages to process at once  |
| `concurrent_handlers`   | `EZQ_CONSUMER_CONCURRENT_HANDLERS`   | 5       | Maximum number of handlers to run concurrently |
| `timeout`               | `EZQ_CONSUMER_TIMEOUT`               | 30      | Timeout for handlers in seconds                |
| `shutdown_grace_period` | `EZQ_CONSUMER_SHUTDOWN_GRACE_PERIOD` | 5       | Grace period for shutdown in seconds           |

### Logging Configuration

Configuration options for logging:

| Parameter             | Environment Variable          | Default  | Description                                       |
| --------------------- | ----------------------------- | -------- | ------------------------------------------------- |
| `level`               | `EZQ_LOG_LEVEL`               | INFO     | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `format`              | `EZQ_LOG_FORMAT`              | standard | Log message format                                |
| `enable_file_logging` | `EZQ_LOG_ENABLE_FILE_LOGGING` | false    | Whether to enable logging to a file               |
| `log_file`            | `EZQ_LOG_FILE`                | None     | Path to the log file                              |

## Example Configuration Scenarios

### Development Environment

```python
from ezvent import configure

# Development configuration
configure(
    queue_host="localhost",
    queue_database="dev_db",
    default_queue_name="dev_events",
    consumer_poll_interval=0.1,  # Quick polling for development
    consumer_concurrent_handlers=1  # Single handler for predictable debugging
)
```

### Production Environment

!!! example ""
    Using environment variables is typically recommended for production:

    ```bash
    # Set in your environment or deployment configuration
    export EZQ_QUEUE_HOST=prod-postgres.internal
    export EZQ_QUEUE_PORT=5432
    export EZQ_QUEUE_USERNAME=app_user
    export EZQ_QUEUE_PASSWORD=secure_password
    export EZQ_QUEUE_DATABASE=events_db
    export EZQ_DEFAULT_QUEUE_NAME=prod_events
    export EZQ_CONSUMER_CONCURRENT_HANDLERS=10
    export EZQ_LOG_LEVEL=WARNING
    ```

### Testing Environment

```python
# In your test setup
from ezvent import configure

# Configure for testing
configure(
    queue_database="test_db",
    default_queue_name="test_events",
    consumer_poll_interval=0.01,  # Fast polling for tests
    consumer_concurrent_handlers=1  # Single handler for predictable behavior
)
```

## Next Steps

Now that you understand how to configure `ezvent`, learn about:

- [Events](events.md): How to define and publish events
- [Handlers](handlers.md): How to handle events

You can also refer to the [API Reference](../api/index.md) for detailed documentation of all configuration options.
