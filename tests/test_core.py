"""Unit tests for core infrastructure modules."""

import asyncio
import tempfile
from pathlib import Path

import pytest

from src.core.cache import TTLCache, cached
from src.core.state import StateManager


class TestStateManager:
    """Tests for StateManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def state_manager(self, temp_dir):
        """Create StateManager instance."""
        return StateManager(temp_dir)

    @pytest.mark.asyncio
    async def test_set_and_get(self, state_manager):
        """Test basic set and get operations."""
        await state_manager.set("test_key", {"value": 123})
        result = await state_manager.get("test_key")
        assert result == {"value": 123}

    @pytest.mark.asyncio
    async def test_get_default(self, state_manager):
        """Test get with default value."""
        result = await state_manager.get("nonexistent", default="default_value")
        assert result == "default_value"

    @pytest.mark.asyncio
    async def test_get_sync(self, state_manager):
        """Test synchronous get from cache."""
        await state_manager.set("cached_key", "cached_value")
        # Should be in cache now
        result = state_manager.get_sync("cached_key")
        assert result == "cached_value"

    @pytest.mark.asyncio
    async def test_delete(self, state_manager):
        """Test delete operation."""
        await state_manager.set("delete_me", "value")
        await state_manager.delete("delete_me")
        result = await state_manager.get("delete_me", default=None)
        assert result is None

    @pytest.mark.asyncio
    async def test_persistence(self, temp_dir):
        """Test that state persists across instances."""
        # Create first instance and set value
        sm1 = StateManager(temp_dir)
        await sm1.set("persistent_key", "persistent_value")

        # Create second instance and retrieve value
        sm2 = StateManager(temp_dir)
        result = await sm2.get("persistent_key")
        assert result == "persistent_value"


class TestTTLCache:
    """Tests for TTLCache class."""

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        """Test basic cache operations."""
        cache = TTLCache(maxsize=10, ttl=60)
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    @pytest.mark.asyncio
    async def test_expiration(self):
        """Test TTL expiration."""
        cache = TTLCache(maxsize=10, ttl=0)  # Immediate expiration
        await cache.set("key1", "value1")
        await asyncio.sleep(0.1)  # Wait for expiration
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        cache = TTLCache(maxsize=2, ttl=60)
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.set("key3", "value3")  # Should evict key1

        result1 = await cache.get("key1")
        result2 = await cache.get("key2")
        result3 = await cache.get("key3")

        assert result1 is None  # Evicted
        assert result2 == "value2"
        assert result3 == "value3"


class TestCachedDecorator:
    """Tests for @cached decorator."""

    @pytest.mark.asyncio
    async def test_caching(self):
        """Test that function results are cached."""
        call_count = 0

        @cached(ttl=60)
        async def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = await expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same argument (should use cache)
        result2 = await expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Not incremented

        # Call with different argument
        result3 = await expensive_function(10)
        assert result3 == 20
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_cache_expiration(self):
        """Test that cache expires after TTL."""
        call_count = 0

        @cached(ttl=0)  # Immediate expiration
        async def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = await expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        await asyncio.sleep(0.1)  # Wait for expiration

        # Second call - cache should be expired
        result2 = await expensive_function(5)
        assert result2 == 10
        assert call_count == 2  # Cache expired, function called again
