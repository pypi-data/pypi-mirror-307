## tested complete 

import pytest
from ratehawk.storage.memory import MemoryStorage

@pytest.fixture
def memory_storage():
    return MemoryStorage()

@pytest.mark.asyncio
async def test_increment(memory_storage):
    key = "test_key"
    count = await memory_storage.increment(key, 60)
    assert count == 1

@pytest.mark.asyncio
async def test_get(memory_storage):
    key = "test_key"
    await memory_storage.increment(key, 60)
    count = await memory_storage.get(key)
    assert count == 1

@pytest.mark.asyncio
async def test_reset(memory_storage):
    key = "test_key"
    await memory_storage.increment(key, 60)
    await memory_storage.reset(key)
    count = await memory_storage.get(key)
    assert count == 0

@pytest.mark.asyncio
async def test_get_tokens(memory_storage):
    key = "test_key"
    await memory_storage.increment(key, 60)
    tokens, last_update = await memory_storage.get_tokens(key)
    assert tokens == 1
    assert last_update > 0

@pytest.mark.asyncio
async def test_set_tokens(memory_storage):
    key = "test_key"
    await memory_storage.set_tokens(key, 5, 1234567890.0)
    tokens, last_update = await memory_storage.get_tokens(key)
    assert tokens == 5
    assert last_update == 1234567890.0

@pytest.mark.asyncio
async def test_distributed_lock(memory_storage):
    key = "test_key"
    async with memory_storage.distributed_lock(key):
        assert True
