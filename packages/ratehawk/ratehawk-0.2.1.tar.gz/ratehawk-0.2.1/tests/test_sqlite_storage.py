import pytest
from ratehawk.storage.sqlite import SQLiteStorage
from ratehawk.exceptions import StorageError

@pytest.fixture
async def sqlite_storage():
    storage = SQLiteStorage(db_path=":memory:")
    await storage._ensure_connection()
    yield storage
    await storage.close()

@pytest.mark.asyncio
async def test_increment(sqlite_storage):
    key = "test_key"
    count = await sqlite_storage.increment(key, 60)
    assert count == 1

@pytest.mark.asyncio
async def test_get(sqlite_storage):
    key = "test_key"
    await sqlite_storage.increment(key, 60)
    count = await sqlite_storage.get(key)
    assert count == 1

@pytest.mark.asyncio
async def test_reset(sqlite_storage):
    key = "test_key"
    await sqlite_storage.increment(key, 60)
    await sqlite_storage.reset(key)
    count = await sqlite_storage.get(key)
    assert count == 0

@pytest.mark.asyncio
async def test_get_tokens(sqlite_storage):
    key = "test_key"
    await sqlite_storage.increment(key, 60)
    tokens, last_update = await sqlite_storage.get_tokens(key)
    assert tokens == 1
    assert last_update > 0

@pytest.mark.asyncio
async def test_set_tokens(sqlite_storage):
    key = "test_key"
    await sqlite_storage.set_tokens(key, 5, 1234567890.0)
    tokens, last_update = await sqlite_storage.get_tokens(key)
    assert tokens == 5
    assert last_update == 1234567890.0

@pytest.mark.asyncio
async def test_distributed_lock(sqlite_storage):
    key = "test_key"
    # Test successful lock acquisition
    async with sqlite_storage.distributed_lock(key):
        # Verify we can't acquire the same lock twice
        with pytest.raises(StorageError):
            async with sqlite_storage.distributed_lock(key):
                pass
    
    # Verify we can acquire the lock again after it's released
    async with sqlite_storage.distributed_lock(key):
        assert True
