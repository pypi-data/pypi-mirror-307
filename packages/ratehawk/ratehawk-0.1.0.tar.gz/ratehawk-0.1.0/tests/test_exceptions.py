import pytest
from ratehawk.exceptions import RateLimitExceeded, StorageError

def test_rate_limit_exceeded():
    with pytest.raises(RateLimitExceeded) as exc_info:
        raise RateLimitExceeded("Rate limit exceeded", retry_after=10)
    assert str(exc_info.value) == "Rate limit exceeded"
    assert exc_info.value.retry_after == 10

def test_storage_error():
    with pytest.raises(StorageError) as exc_info:
        raise StorageError("Storage backend error")
    assert str(exc_info.value) == "Storage backend error"
