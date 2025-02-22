"""
This is an example use for my test, not a part of the lib
"""

import argparse
import asyncio
import multiprocessing
import time

from attr import asdict

from ezq.helper import clean
from ezvent import (
    EZEndEvent,
    EZInterruptEvent,
    EZvent,
    consumer,
    on_event,
    publish_event,
    publish_events,
)


class TutuEvent(EZvent):
    titi: str
    tutu: int


class TotoEvent(TutuEvent):
    test: str


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
    # print("Tutu Event", event)
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


# from ezq import publish_event
# from ezq.events import EZQEndEvent, EZQInterruptEvent


@on_event
async def exit_consumer(event: EZEndEvent):
    print("Exiting consumer...")


async def main(number_of_consumers: int):
    # Publish EZQEndEvent for each consumer
    await asyncio.gather(
        *[consumer() for _ in range(number_of_consumers)],
    )

    print("Exiting main...")


def run_main(number_of_consumers: int):
    asyncio.run(main(number_of_consumers))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Configure event processing parameters."
    )
    parser.add_argument(
        "--num-processes",
        type=int,
        default=1,
        help="Number of parallel processes to run.",
    )
    parser.add_argument(
        "--number-of-consumers",
        type=int,
        default=1,
        help="Number of consumers per process.",
    )
    parser.add_argument(
        "--event-number",
        type=int,
        default=1000,
        help="Total number of events to process.",
    )
    return parser.parse_args()


NUM_PROCESSES: int
NUMBER_OF_CONSUMERS: int
EVENT_NUMBER: int


if __name__ == "__main__":
    args = parse_arguments()
    NUM_PROCESSES = args.num_processes
    NUMBER_OF_CONSUMERS = args.number_of_consumers
    EVENT_NUMBER = args.event_number

    processes: list[multiprocessing.Process] = []

    async def setup():
        await clean()
        await set_queue(EVENT_NUMBER)
        await publish_events(
            [EZEndEvent() for _ in range(NUM_PROCESSES * NUMBER_OF_CONSUMERS * 100)]
        )

    start = time.time()
    asyncio.run(setup())
    setup_time = time.time() - start
    print(f"Setup time: {setup_time}")

    start = time.time()
    for _ in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=run_main, args=(NUMBER_OF_CONSUMERS,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    main_time = time.time() - start
    print(f"Main time: {main_time}")
    print(
        f"Number of events per consumer per second: {EVENT_NUMBER / (main_time * NUMBER_OF_CONSUMERS)}"
    )
    print(
        f"Number of events per parallel worker per second: {EVENT_NUMBER / (main_time * NUM_PROCESSES)}"
    )
    print(f"Number of events per second: {EVENT_NUMBER / main_time}")
    print(
        f"Number of events per consumer per second: {EVENT_NUMBER / (main_time * NUMBER_OF_CONSUMERS)}"
    )
    print(
        f"Number of events per parallel worker per second: {EVENT_NUMBER / (main_time * NUM_PROCESSES)}"
    )
    print(f"Number of events per second: {EVENT_NUMBER / main_time}")
