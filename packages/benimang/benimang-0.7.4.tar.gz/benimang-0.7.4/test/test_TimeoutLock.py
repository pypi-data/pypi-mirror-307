import time
import asyncio
import pytest

from beni.block import TimeoutLock


@pytest.mark.asyncio
async def test_timeout():
    lock = TimeoutLock(timeout=1)
    now = time.time()
    await lock.acquire()
    try:
        async with lock:
            pass
    except TimeoutError:
        dur = time.time() - now
        assert dur >= 1
    lock.release()


@pytest.mark.asyncio
async def test_pass():
    lock = TimeoutLock(timeout=1)
    await lock.acquire()

    async def _releaseLock():
        await asyncio.sleep(0.5)
        lock.release()

    asyncio.create_task(_releaseLock())

    now = time.time()
    async with lock:
        assert time.time() - now >= 0.5


@pytest.mark.asyncio
async def test_timeout_none():
    lock = TimeoutLock()
    await lock.acquire()
    try:
        await asyncio.wait_for(lock.acquire(), timeout=0.5)
    except TimeoutError:
        pass
