from ezvent.events import EZvent
from ezvent.handler import get_event_handler


async def dispatch_event(event: EZvent, *, timeout: float) -> None:
    await get_event_handler().handle_event(event, timeout=timeout)
