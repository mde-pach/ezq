import asyncio
import logging
from dataclasses import dataclass

from ezq import (
    EZQEndEvent,
    EZQEvent,
    EZQInterruptEvent,
    clean,
    consumer,
    on_event,
    process_event,
)
from ezq.processor import process_events


@dataclass
class TutuEvent(EZQEvent):
    titi: str
    tutu: int


@dataclass
class TotoEvent(TutuEvent):
    pass


@on_event
async def tutu_event(event: TutuEvent):
    pass
    # print("Tutu Event", event)
    # await asyncio.sleep(100)


# @on_event
# async def tutu2_event(event: TutuEvent):
#     print("Tutu2 Event", event)
#     await asyncio.sleep(100)


@on_event
async def toto_event(event: TotoEvent):
    pass
    # print("Toto Event", event)


stop_event = asyncio.Event()


async def main():
    import time

    logging.basicConfig(level=logging.INFO)

    await clean()

    start = time.time()
    total_tutu_events = 100000
    number_of_consumers = 2
    # for _ in range(total_tutu_events):
    #     await process_event(TutuEvent(titi="titi", tutu=1))
    await process_events(
        [TutuEvent(titi="titi", tutu=1) for _ in range(total_tutu_events)],
    )
    for _ in range(number_of_consumers):
        await process_event(EZQEndEvent())
    total_events = total_tutu_events + 1
    event_processing_time = time.time() - start
    average_event_time = event_processing_time / total_events
    print("Total event processing time:", event_processing_time)
    print("Average event processing time per event:", average_event_time)

    start = time.time()
    await asyncio.gather(
        *[consumer() for _ in range(number_of_consumers)],
    )
    consumer_time = time.time() - start

    print(f"Event processing time: {event_processing_time}")
    print(f"Consumer time: {consumer_time}")


if __name__ == "__main__":
    asyncio.run(main())
