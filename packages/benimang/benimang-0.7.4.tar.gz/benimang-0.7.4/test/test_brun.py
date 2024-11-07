import pytest

from beni import bpath
from beni.brun import run


@pytest.mark.asyncio
async def test_run():
    result, code = await run('dir', bpath.desktop())
    assert code == 0
    assert '的目录' in result
