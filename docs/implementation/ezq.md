# Message Queue Component

This document describes the underlying message queue component of the ezvent framework. This queue system provides message storage and processing capabilities through PostgreSQL with PGMQ extension.

## Overview

The message queue component serves as the reliable storage layer within ezvent's architecture. It handles the persistence and retrieval of events through a PostgreSQL database.

## Key Features

- **PostgreSQL Backend**: Message storage using PostgreSQL
- **PGMQ Integration**: Queue functionality through PGMQ extension
- **Async Support**: Native asyncio integration
- **Transaction Support**: Message delivery with database transactions

## Internal Architecture

### Message Flow

**Event Production**:
- ezvent events are serialized to messages
- Messages are stored in PostgreSQL using PGMQ

**Message Storage**:
- Messages are stored in PGMQ queues
- Each queue is a separate table in PostgreSQL
- Messages maintain FIFO order

**Event Consumption**:
- Consumer polls for new messages
- Messages are processed in batches

### Internal Components

#### Queue Manager

Handles internal queue operations:

- Queue creation and management
- Message enqueueing
- Connection management

#### Message Consumer

Manages message processing:

- Message polling
- Batch processing
- Basic error handling

## Error Handling

The queue system handles errors through PostgreSQL transaction management:

- Messages are only removed after successful processing
- Failed transactions are rolled back

## Configuration Reference

All configuration is handled through ezvent's configuration system. Despite ezvent being the main framework, the current environment variable naming still uses legacy prefixes:

### Queue Settings

| Option                 | Environment Variable             | Default   | Description                         |
| ---------------------- | -------------------------------- | --------- | ----------------------------------- |
| host                   | EZQ_QUEUE_HOST                   | localhost | PostgreSQL host                     |
| port                   | EZQ_QUEUE_PORT                   | 5432      | PostgreSQL port                     |
| username               | EZQ_QUEUE_USERNAME               | postgres  | PostgreSQL username                 |
| password               | EZQ_QUEUE_PASSWORD               | postgres  | PostgreSQL password                 |
| database               | EZQ_QUEUE_DATABASE               | postgres  | PostgreSQL database                 |
| default_queue_name     | EZQ_DEFAULT_QUEUE_NAME           | ezq       | Default queue name                  |
| connection_timeout     | EZQ_QUEUE_CONNECTION_TIMEOUT     | 10        | Connection timeout in seconds       |
| connection_retries     | EZQ_QUEUE_CONNECTION_RETRIES     | 3         | Number of connection retry attempts |
| connection_retry_delay | EZQ_QUEUE_CONNECTION_RETRY_DELAY | 1         | Delay between retries in seconds    |

### Consumer Settings

| Option                | Environment Variable               | Default | Description                         |
| --------------------- | ---------------------------------- | ------- | ----------------------------------- |
| poll_interval         | EZQ_CONSUMER_POLL_INTERVAL         | 1.0     | Time in seconds between empty polls |
| batch_size            | EZQ_CONSUMER_BATCH_SIZE            | 10      | Maximum messages per batch          |
| concurrent_handlers   | EZQ_CONSUMER_CONCURRENT_HANDLERS   | 5       | Maximum concurrent handlers         |
| timeout               | EZQ_CONSUMER_TIMEOUT               | 30      | Event processing timeout            |
| shutdown_grace_period | EZQ_CONSUMER_SHUTDOWN_GRACE_PERIOD | 5       | Shutdown grace period in seconds    |

### Logging Settings

| Option              | Environment Variable        | Default  | Description                         |
| ------------------- | --------------------------- | -------- | ----------------------------------- |
| level               | EZQ_LOG_LEVEL               | INFO     | Logging level                       |
| format              | EZQ_LOG_FORMAT              | standard | Log format                          |
| enable_file_logging | EZQ_LOG_ENABLE_FILE_LOGGING | false    | Whether to enable logging to a file |
| log_file            | EZQ_LOG_FILE                | None     | Path to the log file                |

## Best Practices

1. **Queue Management**:

   - Monitor queue sizes
   - Set appropriate batch sizes

2. **Performance**:
   - Configure concurrent handlers based on workload
   - Balance batch size with processing requirements
