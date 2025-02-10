"""
This is an example use for my test, not a part of the lib
"""

import asyncio
from dataclasses import dataclass

from ezq import EZQEndEvent, EZQEvent, consumer, on_event, publish_event, publish_events
from ezq.helper import clean


@dataclass
class TutuEvent(EZQEvent):
    titi: str
    tutu: int


@dataclass
class TotoEvent(TutuEvent):
    pass


# @on_event
# async def tutu2_event(event: TutuEvent):
#     print("Tutu2 Event", event)
#     await asyncio.sleep(100)


@on_event
async def toto_event(event: TotoEvent):
    pass
    # print("Toto Event", event)


stop_event = asyncio.Event()


@on_event
async def tutu_event(event: TutuEvent):
    pass
    # stop_event.set()
    # raise ValueError
    print("Tutu Event", event)
    # await asyncio.sleep(100)


async def set_queue(amount: int):
    await clean()
    await publish_events(
        [TutuEvent(titi="titi", tutu=_) for _ in range(amount)],
    )


total_tutu_events = 100000


# async def main():
#     import time

#     # logging.basicConfig(level=logging.DEBUG)
#     # await clean()
#     await set_queue(total_tutu_events)

#     start = time.time()
#     number_of_consumers = 10

#     # for _ in range(number_of_consumers):
#     #     await publish_event(EZQEndEvent())

#     # total_events = total_tutu_events + 1
#     # event_processing_time = time.time() - start
#     # average_event_time = event_processing_time / total_events

#     # print("Total event processing time:", event_processing_time)
#     # print("Average event processing time per event:", average_event_time)

#     start = time.time()
#     await asyncio.gather(
#         *[consumer(stop_event=stop_event) for _ in range(number_of_consumers)],
#     )
#     consumer_time = time.time() - start

#     # print(f"Event processing time: {event_processing_time}")
#     print(f"Consumer time: {consumer_time}")


from ezq import publish_event
from ezq.events import EZQEndEvent, EZQInterruptEvent


@on_event
async def exit_consumer(event: EZQEndEvent):
    print("Exiting consumer...")


async def main():
    await clean()
    await set_queue(1000)
    await publish_event(EZQEndEvent())
    await consumer()

    print("Exiting main...")


if __name__ == "__main__":
    asyncio.run(main())
