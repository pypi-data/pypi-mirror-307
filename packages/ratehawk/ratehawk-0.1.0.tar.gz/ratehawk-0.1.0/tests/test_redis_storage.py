import pytest
from redis import Redis
from ratehawk.storage.redis import RedisStorage

@pytest.fixture
def redis_storage():
    redis_client = Redis(host='localhost', port=6379, db=0)
    return RedisStorage(redis_client)

@pytest.mark.asyncio
async def test_increment(redis_storage):
    key = "test_key"
    count = await redis_storage.increment(key, 60)
    assert count == 1

@pytest.mark.asyncio
async def test_get(redis_storage):
    key = "test_key"
    await redis_storage.increment(key, 60)
    count = await redis_storage.get(key)
    assert count == 1

@pytest.mark.asyncio
async def test_reset(redis_storage):
    key = "test_key"
    await redis_storage.increment(key, 60)
    await redis_storage.reset(key)
    count = await redis_storage.get(key)
    assert count == 0

@pytest.mark.asyncio
async def test_get_tokens(redis_storage):
    key = "test_key"
    await redis_storage.increment(key, 60)
    tokens, last_update = await redis_storage.get_tokens(key)
    assert tokens == 1
    assert last_update > 0

@pytest.mark.asyncio
async def test_set_tokens(redis_storage):
    key = "test_key"
    await redis_storage.set_tokens(key, 5, 1234567890.0)
    tokens, last_update = await redis_storage.get_tokens(key)
    assert tokens == 5
    assert last_update == 1234567890.0

@pytest.mark.asyncio
async def test_distributed_lock(redis_storage):
    key = "test_key"
    async with redis_storage.distributed_lock(key):
        assert True
