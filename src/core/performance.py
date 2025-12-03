"""Performance monitoring utilities for the E-Ink dashboard application.

This module provides decorators and utilities for monitoring function execution time,
memory usage, and other performance metrics.
"""

import functools
import inspect
import logging
import time
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def measure_time(func: F) -> F:
    """Decorator to measure and log function execution time.

    Works with both sync and async functions.

    Usage:
        @measure_time
        async def slow_function():
            await asyncio.sleep(1)
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"⏱️  {func.__name__} took {elapsed:.3f}s")

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"⏱️  {func.__name__} took {elapsed:.3f}s")

    if inspect.iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    else:
        return sync_wrapper  # type: ignore


def log_slow_operations(threshold_seconds: float = 1.0):
    """Decorator to log operations that exceed a time threshold.

    Args:
        threshold_seconds: Time threshold in seconds

    Usage:
        @log_slow_operations(threshold_seconds=0.5)
        async def potentially_slow():
            ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            if elapsed > threshold_seconds:
                logger.warning(
                    f"⚠️  Slow operation: {func.__name__} took {elapsed:.3f}s "
                    f"(threshold: {threshold_seconds}s)"
                )
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            if elapsed > threshold_seconds:
                logger.warning(
                    f"⚠️  Slow operation: {func.__name__} took {elapsed:.3f}s "
                    f"(threshold: {threshold_seconds}s)"
                )
            return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


class PerformanceMonitor:
    """Context manager for monitoring performance of code blocks.

    Usage:
        with PerformanceMonitor("data_fetch"):
            data = fetch_data()

        async with PerformanceMonitor("async_operation"):
            result = await async_operation()
    """

    def __init__(self, operation_name: str, log_level: int = logging.INFO):
        self.operation_name = operation_name
        self.log_level = log_level
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        logger.log(self.log_level, f"⏱️  {self.operation_name} took {elapsed:.3f}s")
        return False

    async def __aenter__(self):
        self.start_time = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        logger.log(self.log_level, f"⏱️  {self.operation_name} took {elapsed:.3f}s")
        return False
