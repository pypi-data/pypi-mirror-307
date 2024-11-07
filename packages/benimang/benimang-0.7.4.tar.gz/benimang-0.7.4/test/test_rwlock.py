import asyncio
import time

import pytest

from beni.block import RWLock

_result: str = ''
_timeAry: list[float] = []
_lock: RWLock = RWLock()


@pytest.mark.asyncio
async def test():
    asyncio.create_task(_read())
    await asyncio.sleep(0.1)
    await asyncio.gather(_read(), _write())
    assert 0.09 <= _timeAry[1] - _timeAry[0]
    assert _result == 'rrw'


async def _read():
    async with _lock.useRead():
        await asyncio.sleep(0.5)
        global _result, _timeAry
        _result += 'r'
        _timeAry.append(time.time())


async def _write():
    async with _lock.useWrite():
        global _result
        _result += 'w'
        _timeAry.append(time.time())
