import pytest
from ratehawk.storage.postgres import PostgresStorage

@pytest.fixture
async def postgres_storage():
    storage = PostgresStorage(dsn="postgresql://localhost/ratehawk_test")
    await storage._ensure_pool()
    yield storage
    await storage.close()

@pytest.mark.asyncio
async def test_increment(postgres_storage):
    key = "test_key"
    count = await postgres_storage.increment(key, 60)
    assert count == 1

@pytest.mark.asyncio
async def test_get(postgres_storage):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    count = await postgres_storage.get(key)
    assert count == 1

@pytest.mark.asyncio
async def test_reset(postgres_storage):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    await postgres_storage.reset(key)
    count = await postgres_storage.get(key)
    assert count == 0

@pytest.mark.asyncio
async def test_get_tokens(postgres_storage):
    key = "test_key"
    await postgres_storage.increment(key, 60)
    tokens, last_update = await postgres_storage.get_tokens(key)
    assert tokens == 1
    assert last_update > 0

@pytest.mark.asyncio
async def test_set_tokens(postgres_storage):
    key = "test_key"
    await postgres_storage.set_tokens(key, 5, 1234567890.0)
    tokens, last_update = await postgres_storage.get_tokens(key)
    assert tokens == 5
    assert last_update == 1234567890.0

@pytest.mark.asyncio
async def test_distributed_lock(postgres_storage):
    key = "test_key"
    async with postgres_storage.distributed_lock(key):
        assert True
