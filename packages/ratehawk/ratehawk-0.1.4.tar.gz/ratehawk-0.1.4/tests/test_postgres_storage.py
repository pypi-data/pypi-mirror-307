## tested complete 

import pytest
from ratehawk.storage.postgres import PostgresStorage

@pytest.fixture
async def postgres_storage():
    storage = PostgresStorage(dsn="postgresql://localhost/ratehawk_test")
    await storage._ensure_pool()
    # Clear the table before each test
    async with storage._pool.acquire() as conn:
        await conn.execute("DELETE FROM rate_limits")
    return storage

@pytest.fixture
async def cleanup(postgres_storage):
    yield
    # Clear the table after each test
    async with postgres_storage._pool.acquire() as conn:
        await conn.execute("DELETE FROM rate_limits")
    await postgres_storage.close()

@pytest.mark.asyncio
async def test_increment(postgres_storage, cleanup):
    key = "test_key"
    count = await postgres_storage.increment(key, 60)
    assert count == 1

@pytest.mark.asyncio
async def test_get(postgres_storage, cleanup):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    count = await postgres_storage.get(key)
    assert count == 1

@pytest.mark.asyncio
async def test_reset(postgres_storage, cleanup):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    await postgres_storage.reset(key)
    count = await postgres_storage.get(key)
    assert count == 0

@pytest.mark.asyncio
async def test_get_tokens(postgres_storage, cleanup):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    tokens, last_update = await postgres_storage.get_tokens(key)
    assert tokens == 1
    assert last_update > 0

@pytest.mark.asyncio
async def test_set_tokens(postgres_storage, cleanup):
    key = "test_key"
    await postgres_storage.set_tokens(key, 5, 1234567890.0)
    tokens, last_update = await postgres_storage.get_tokens(key)
    assert tokens == 5
    assert last_update == 1234567890.0

@pytest.mark.asyncio
async def test_distributed_lock(postgres_storage, cleanup):
    key = "test_key"
    async with postgres_storage.distributed_lock(key):
        assert True
