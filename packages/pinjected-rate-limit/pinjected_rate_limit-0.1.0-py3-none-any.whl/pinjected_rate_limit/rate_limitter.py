import asyncio
from dataclasses import dataclass, field
from datetime import timedelta, datetime
from pinjected import *

class AsyncRateLimit:
    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@dataclass
class AsyncResourceLockHandle:
    amount: int
    src: "AsyncResourceLimit"

    async def __aenter__(self):
        await self.src.acquire(self.amount)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@dataclass
class AsyncResourceLimit:
    max_resource: int
    duration: timedelta
    waiting_queue: list[int, asyncio.Event] = field(default_factory=list)
    usage: list[(datetime, int)] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    invoke_task: asyncio.Task = field(default=None)

    def get(self, amount):
        return AsyncResourceLockHandle(amount, self)

    def _get_current_usage(self):
        consumed = 0
        now = datetime.now()
        expiration = now - self.duration
        non_expired = [(time, amount) for time, amount in self.usage if time >= expiration]
        for time, amount in non_expired:
            consumed += amount
        self.usage = non_expired
        return consumed

    async def invoke_waiters(self):
        async def task():
            while True:
                while self.waiting_queue:
                    amt, event = self.waiting_queue[0]
                    current_usage = self._get_current_usage()
                    if amt + current_usage <= self.max_resource:
                        self.usage.append((datetime.now(), amt))
                        self.waiting_queue.pop(0)
                        event.set()
                    else:
                        await asyncio.sleep(1)
                await asyncio.sleep(1)
        if self.invoke_task is None:
            self.invoke_task = asyncio.create_task(task())

    async def acquire(self, resource_amount: int):
        event = asyncio.Event()
        self.waiting_queue.append((resource_amount, event))
        await self.invoke_waiters()
        await event.wait()

@instance
async def test_rate_limit():
    limit = AsyncResourceLimit(5, timedelta(seconds=6))
    from loguru import logger
    async def task1():
        async with limit.get(2) :
            logger.info("task1 acquired 2")
            await asyncio.sleep(5)
    async def task2():
        async with limit.get(3) :
            logger.info("task2 acquired 3")
            await asyncio.sleep(5)
    async def task3():
        async with limit.get(2) :
            logger.info("task3 acquired 2")
            await asyncio.sleep(5)
    await asyncio.gather(task1(), task2(), task3())
__meta_design__ = design(
    overrides=design(
    )
)