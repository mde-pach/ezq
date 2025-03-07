# Event Handlers

Event handlers are functions that process events when they occur. They contain the business logic that responds to events in your system.

## Defining Handlers

In EZQ, event handlers are defined using the `@on_event` decorator:

```python
from ezq import on_event
from my_events import UserCreatedEvent

@on_event
async def send_welcome_email(event: UserCreatedEvent):
    """Send a welcome email when a new user is created"""
    print(f"Sending welcome email to {event.email}")
    # Code to send email...
```

Key points about handlers:

- Handlers must be **async functions**
- The first parameter should be the event type the handler processes
- The event type annotation is used to determine which events the handler can process
- Multiple handlers can be registered for the same event type

## Handler Registration

Handlers are automatically registered with EZQ when the `@on_event` decorator is applied. The handler will be called whenever an event of the specified type is processed.

### Handler Discovery

For handlers to be registered, the module containing them must be imported before events are processed. A common pattern is to import all handlers in your application's entry point:

```python
# app.py - main entry point
import asyncio
from ezq import consumer

# Import all handlers to ensure they are registered
import handlers.user_handlers
import handlers.order_handlers
import handlers.notification_handlers

async def main():
    await consumer()

if __name__ == "__main__":
    asyncio.run(main())
```

## Multiple Handlers for One Event

You can define multiple handlers for the same event type. Each handler will be called when the event is processed:

```python
@on_event
async def send_welcome_email(event: UserCreatedEvent):
    """Send a welcome email when a new user is created"""
    print(f"Sending welcome email to {event.email}")

@on_event
async def notify_admin(event: UserCreatedEvent):
    """Notify admin about new user registrations"""
    print(f"Admin notification: New user {event.username} created")

@on_event
async def update_user_metrics(event: UserCreatedEvent):
    """Update metrics dashboard with new user count"""
    print(f"Updating metrics for new user {event.user_id}")
```

## Generic Handlers

You can create generic handlers that process multiple event types:

```python
@on_event
async def log_all_events(event):
    """Log all events that occur in the system"""
    print(f"Event occurred: {event.__class__.__name__} - {event}")
```

A handler without a specific type annotation will be called for all event types.

## Handler Context

Handlers run in the context of the consumer that processes the event. The consumer provides:

- **Concurrency control**: Multiple handlers can run concurrently
- **Timeout management**: Handlers are subject to a timeout
- **Error handling**: Errors in handlers are caught and logged

## Event Processing Order

When an event is processed:

1. The consumer retrieves the event from the queue
2. The dispatcher determines which handlers should process the event
3. Each handler is executed in a separate task
4. The consumer waits for all handler tasks to complete (or time out)
5. The event is acknowledged (deleted from the queue)

## Handler Failures

If a handler raises an exception:

1. The exception is logged
2. Other handlers for the same event continue to execute
3. The event is still acknowledged (deleted from the queue)

If you need to ensure that an event is reprocessed if a handler fails, you'll need to implement custom error handling.

## Advanced Handler Patterns

### Chain of Responsibility

You can implement a chain of responsibility by having handlers publish new events:

```python
@on_event
async def process_order(event: OrderPlacedEvent):
    """Process a new order"""
    # Process the order
    print(f"Processing order {event.order_id}")

    # Publish a new event to trigger the next step
    await publish_event(PaymentRequiredEvent(
        order_id=event.order_id,
        amount=event.total_amount
    ))

@on_event
async def process_payment(event: PaymentRequiredEvent):
    """Process payment for an order"""
    # Process the payment
    print(f"Processing payment of ${event.amount} for order {event.order_id}")

    # Publish a new event to trigger the next step
    await publish_event(OrderFulfilledEvent(
        order_id=event.order_id
    ))
```

### Event Sourcing

Event sourcing is a pattern where the state of your application is determined by a sequence of events. EZQ can be used as part of an event sourcing architecture:

```python
class UserAggregate:
    def __init__(self, user_id):
        self.user_id = user_id
        self.username = None
        self.email = None
        self.is_active = False

    async def apply_events(self):
        """Apply all events for this user from the event store"""
        events = await get_events_for_user(self.user_id)
        for event in events:
            self.apply_event(event)

    def apply_event(self, event):
        """Apply a single event to update the aggregate state"""
        if isinstance(event, UserCreatedEvent):
            self.username = event.username
            self.email = event.email
            self.is_active = True
        elif isinstance(event, UserEmailChangedEvent):
            self.email = event.new_email
        elif isinstance(event, UserDeactivatedEvent):
            self.is_active = False
```

## Best Practices

### Keep Handlers Focused

Each handler should have a single responsibility. If you find a handler doing multiple things, consider splitting it into multiple handlers.

### Handle Errors Gracefully

Always handle errors in your handlers to prevent them from crashing the consumer:

```python
@on_event
async def send_welcome_email(event: UserCreatedEvent):
    try:
        # Attempt to send the email
        await email_service.send_welcome_email(event.email)
    except EmailServiceError as e:
        # Log the error but don't crash
        logger.error(f"Failed to send welcome email to {event.email}: {e}")
        # Maybe publish a notification event for the failure
        await publish_event(EmailFailedEvent(
            email=event.email,
            error=str(e)
        ))
```

### Use Handler Dependencies

For handlers that need external services, consider using dependency injection or creating handler factory functions:

```python
def create_email_handler(email_service):
    @on_event
    async def send_welcome_email(event: UserCreatedEvent):
        await email_service.send_welcome_email(event.email)
    return send_welcome_email

# Create the handler with a specific email service
send_welcome_email = create_email_handler(my_email_service)
```

### Monitor Handler Performance

Add timing and monitoring to your handlers to track their performance:

```python
import time
import logging

logger = logging.getLogger(__name__)

@on_event
async def process_order(event: OrderPlacedEvent):
    start_time = time.time()

    # Process the order
    await process_order_logic(event)

    execution_time = time.time() - start_time
    logger.info(f"Processed order {event.order_id} in {execution_time:.2f} seconds")
```

## Next Steps

Now that you understand how to create and use event handlers, learn about:

- [Events](events.md): How to define and publish events
- [Configuration](configuration.md): How to configure the event system
