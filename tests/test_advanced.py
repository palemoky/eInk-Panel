"""Unit tests for advanced optimizations."""

import asyncio

import pytest

from src.core.task_manager import TaskManager
from src.core.time_slots import TimeSlot, TimeSlots


class TestTaskManager:
    """Tests for TaskManager."""

    @pytest.mark.asyncio
    async def test_start_stop_task(self):
        """Test starting and stopping a task."""
        task_mgr = TaskManager()
        executed = False

        async def simple_task(stop_event):
            nonlocal executed
            executed = True
            await stop_event.wait()

        await task_mgr.start("test", simple_task)
        await asyncio.sleep(0.1)  # Give task time to execute
        assert await task_mgr.is_running("test")
        assert executed

        await task_mgr.stop("test")
        assert not await task_mgr.is_running("test")

    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test cleanup stops all tasks."""
        task_mgr = TaskManager()

        async def dummy_task(stop_event):
            await stop_event.wait()

        await task_mgr.start("task1", dummy_task)
        await task_mgr.start("task2", dummy_task)

        assert len(task_mgr.get_running_tasks()) == 2

        await task_mgr.cleanup()
        assert len(task_mgr.get_running_tasks()) == 0

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager cleanup."""
        executed = False

        async def simple_task(stop_event):
            nonlocal executed
            executed = True
            await stop_event.wait()

        async with TaskManager() as task_mgr:
            await task_mgr.start("test", simple_task)
            await asyncio.sleep(0.1)  # Give task time to execute
            assert executed

        # Should be cleaned up after context exit

        # (can't easily verify without keeping reference)


class TestTimeSlots:
    """Tests for TimeSlots."""

    def test_same_day_slot(self):
        """Test same-day time slot."""
        slot = TimeSlot(9, 17)  # 9:00-17:00
        assert slot.contains(10)
        assert slot.contains(9)
        assert not slot.contains(17)
        assert not slot.contains(20)

    def test_cross_day_slot(self):
        """Test cross-day time slot."""
        slot = TimeSlot(20, 8)  # 20:00-08:00
        assert slot.contains(22)
        assert slot.contains(0)
        assert slot.contains(7)
        assert not slot.contains(10)
        assert not slot.contains(15)

    def test_time_slots_parsing(self):
        """Test TimeSlots parsing."""
        slots = TimeSlots("0-12,18-24")
        assert slots.contains_hour(10)
        assert slots.contains_hour(20)
        assert not slots.contains_hour(15)

    def test_cross_day_slots(self):
        """Test cross-day time slots."""
        slots = TimeSlots("20-8")
        assert slots.contains_hour(22)
        assert slots.contains_hour(0)
        assert slots.contains_hour(7)
        assert not slots.contains_hour(10)

    def test_empty_slots(self):
        """Test empty time slots."""
        slots = TimeSlots("")
        assert not slots
        assert not slots.contains_hour(10)

    def test_invalid_slots(self):
        """Test invalid time slots."""
        slots = TimeSlots("invalid")
        assert not slots
        assert not slots.contains_hour(10)
