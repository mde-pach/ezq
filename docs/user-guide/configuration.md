# Configuration

EZQ provides a flexible configuration system that allows you to customize its behavior according to your needs.

## Configuration Methods

There are two primary ways to configure EZQ:

1. **Environment Variables**: Set environment variables with the `EZQ_` prefix
2. **Programmatic Configuration**: Configure directly in code using the `configure()` function

## Configuration Precedence

When determining the value for a configuration option, EZQ follows this precedence order:

1. Programmatic configuration (highest priority)
2. Environment variables
3. Default values (lowest priority)

## Using Environment Variables

Environment variables are an excellent way to configure EZQ in production environments. All configuration options can be set using environment variables with the `EZQ_` prefix.

```bash
# PostgreSQL connection settings
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

For more dynamic configurations or when you need to set configuration values at runtime, you can use the `configure()` function:

```python
import ezq

# Configure specific parameters
ezq.configure(
    queue_host="postgres.example.com",
    queue_username="app_user",
    queue_password="secure_password",
    consumer_batch_size=20
)
```

The `configure()` function accepts keyword arguments for any configuration option. The naming convention follows the pattern:

- `queue_*` for queue-related settings
- `consumer_*` for consumer-related settings
- `logging_*` for logging-related settings

## Configuration Options

### Queue Configuration

| Option                   | Environment Variable               | Default   | Description                         |
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

| Option                  | Environment Variable                 | Default | Description                                        |
| ----------------------- | ------------------------------------ | ------- | -------------------------------------------------- |
| `poll_interval`         | `EZQ_CONSUMER_POLL_INTERVAL`         | 1.0     | Time in seconds to wait between empty polls        |
| `batch_size`            | `EZQ_CONSUMER_BATCH_SIZE`            | 10      | Maximum number of messages to process in a batch   |
| `concurrent_handlers`   | `EZQ_CONSUMER_CONCURRENT_HANDLERS`   | 5       | Maximum number of handlers to execute concurrently |
| `timeout`               | `EZQ_CONSUMER_TIMEOUT`               | 30      | Default timeout for event processing               |
| `shutdown_grace_period` | `EZQ_CONSUMER_SHUTDOWN_GRACE_PERIOD` | 5       | Grace period for shutdown in seconds               |

### Logging Configuration

| Option                | Environment Variable          | Default         | Description                                       |
| --------------------- | ----------------------------- | --------------- | ------------------------------------------------- |
| `level`               | `EZQ_LOG_LEVEL`               | INFO            | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `format`              | `EZQ_LOG_FORMAT`              | standard format | Log message format                                |
| `enable_file_logging` | `EZQ_LOG_ENABLE_FILE_LOGGING` | false           | Whether to enable logging to a file               |
| `log_file`            | `EZQ_LOG_FILE`                | None            | Path to the log file                              |

## Configuration in Different Environments

### Development

For development, you can use a combination of environment variables and programmatic configuration:

```python
# development_config.py
import ezq
import os

# Load development environment
if os.getenv("ENV") == "development":
    ezq.configure(
        queue_host="localhost",
        queue_password="dev_password",
        consumer_batch_size=1,  # Process one message at a time for easier debugging
        logging_level="DEBUG"
    )
```

### Production

For production, it's generally best to use environment variables:

```bash
# production.env
EZQ_QUEUE_HOST=production-db.example.com
EZQ_QUEUE_USERNAME=app_user
EZQ_QUEUE_PASSWORD=secure_production_password
EZQ_CONSUMER_BATCH_SIZE=50
EZQ_CONSUMER_CONCURRENT_HANDLERS=20
EZQ_LOG_LEVEL=WARNING
```

### Docker/Kubernetes

When running in containerized environments, you can pass environment variables through your Docker or Kubernetes configuration:

```yaml
# docker-compose.yml
version: "3"
services:
  app:
    image: my-ezq-app
    environment:
      - EZQ_QUEUE_HOST=postgres
      - EZQ_QUEUE_PASSWORD=my_password
      - EZQ_DEFAULT_QUEUE_NAME=app_events
```

## Accessing Configuration Values

If you need to access the current configuration values in your code, you can use `get_config()`:

```python
from ezq import get_config

config = get_config()
print(f"Current host: {config.queue.host}")
print(f"Batch size: {config.consumer.batch_size}")
```

## Reloading Configuration

You can reload the configuration at runtime by calling `get_config()` with `reload=True`:

```python
from ezq import get_config

# Reload configuration (e.g., after environment variables have changed)
config = get_config(reload=True)
```

## Best Practices

- Use environment variables for production deployments
- Keep sensitive information (like passwords) in environment variables, not in code
- Consider using a secrets manager for sensitive configuration in production
- Use different queue names for different environments to avoid cross-environment pollution
- Set appropriate logging levels for different environments
