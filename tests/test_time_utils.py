"""Tests for time utilities."""

import pendulum

from src.core.time_utils import QuietHours


class TestQuietHours:
    """Tests for QuietHours class."""

    def test_check_not_quiet(self):
        """Test when current time is not in quiet hours."""
        quiet = QuietHours(start_hour=1, end_hour=6, timezone="UTC")

        # Test time outside quiet hours
        current_time = pendulum.parse("2024-01-01 12:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

        current_time = pendulum.parse("2024-01-01 20:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

    def test_check_in_quiet_hours(self):
        """Test when current time is in quiet hours."""
        quiet = QuietHours(start_hour=1, end_hour=6, timezone="UTC")

        # Test times in quiet hours
        current_time = pendulum.parse("2024-01-01 02:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert is_quiet
        assert sleep_seconds > 0  # Should have time until 06:00

        current_time = pendulum.parse("2024-01-01 05:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert is_quiet
        assert sleep_seconds > 0

    def test_check_cross_midnight(self):
        """Test quiet hours that cross midnight."""
        quiet = QuietHours(start_hour=22, end_hour=6, timezone="UTC")

        # Before midnight
        current_time = pendulum.parse("2024-01-01 23:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert is_quiet
        assert sleep_seconds > 0

        # After midnight
        current_time = pendulum.parse("2024-01-01 03:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert is_quiet
        assert sleep_seconds > 0

        # Outside quiet hours
        current_time = pendulum.parse("2024-01-01 12:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

    def test_check_boundary_start(self):
        """Test boundary at start hour."""
        quiet = QuietHours(start_hour=1, end_hour=6, timezone="UTC")

        # Exactly at start hour
        current_time = pendulum.parse("2024-01-01 01:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert is_quiet
        assert sleep_seconds > 0

    def test_check_boundary_end(self):
        """Test boundary at end hour."""
        quiet = QuietHours(start_hour=1, end_hour=6, timezone="UTC")

        # Exactly at end hour (should not be quiet)
        current_time = pendulum.parse("2024-01-01 06:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

    def test_same_start_and_end(self):
        """Test when start and end hours are the same."""
        quiet = QuietHours(start_hour=6, end_hour=6, timezone="UTC")

        # Should never be quiet
        current_time = pendulum.parse("2024-01-01 06:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

        current_time = pendulum.parse("2024-01-01 12:00:00", tz="UTC")
        is_quiet, sleep_seconds = quiet.check(current_time)
        assert not is_quiet
        assert sleep_seconds == 0

    def test_repr(self):
        """Test string representation."""
        quiet = QuietHours(start_hour=1, end_hour=6, timezone="UTC")
        repr_str = repr(quiet)
        assert "01:00-06:00" in repr_str
        assert "UTC" in repr_str
