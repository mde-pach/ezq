import asyncio

from _main import TutuEvent
from ezq import EZQEndEvent, EZQEvent, clean, consumer, on_event, process_events


async def set_queue(amount: int):
    await clean()
    await process_events(
        [TutuEvent(titi="titi", tutu=_) for _ in range(amount)],
    )


async def main():
    await set_queue(10000)


if __name__ == "__main__":
    asyncio.run(main())
