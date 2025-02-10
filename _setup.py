"""
This is an example use for my test, not a part of the lib
"""

import asyncio

from _main import TutuEvent
from ezq import publish_events
from ezq.helper import clean


async def set_queue(amount: int):
    await clean()
    await publish_events(
        [TutuEvent(titi="titi", tutu=_) for _ in range(amount)],
    )


async def main():
    await set_queue(10000)


if __name__ == "__main__":
    asyncio.run(main())
