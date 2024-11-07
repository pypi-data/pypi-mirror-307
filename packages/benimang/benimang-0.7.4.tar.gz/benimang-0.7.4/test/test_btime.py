import datetime

import pytest

from beni.btime import networkTime


@pytest.mark.asyncio
async def test_networkTime():
    result = await networkTime()
    assert type(result) is datetime.datetime
    assert abs((datetime.datetime.now() - result).total_seconds()) < 5 * 60  # 与本地时间误差5分钟
