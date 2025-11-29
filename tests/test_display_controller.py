"""Tests for display controller."""

import pendulum

from src.core.display_controller import DisplayController


class TestDisplayController:
    """Tests for DisplayController class."""

    def test_get_current_mode_default(self):
        """Test default mode when no special conditions."""
        controller = DisplayController()

        # Regular day
        now = pendulum.parse("2024-06-15 12:00:00")
        mode = controller.get_current_mode(now)
        assert mode == "dashboard"

    def test_get_current_mode_year_end(self):
        """Test year-end mode on December 31st."""
        controller = DisplayController()

        # December 31st
        now = pendulum.parse("2024-12-31 12:00:00")
        mode = controller.get_current_mode(now)
        assert mode == "year_end"

    def test_get_refresh_interval_dashboard(self):
        """Test refresh interval for dashboard mode."""
        controller = DisplayController()

        interval = controller.get_refresh_interval("dashboard")
        assert interval > 0
        assert isinstance(interval, int)

    def test_get_refresh_interval_quote(self):
        """Test refresh interval for quote mode."""
        controller = DisplayController()

        interval = controller.get_refresh_interval("quote")
        assert interval > 0
        assert isinstance(interval, int)

    def test_get_refresh_interval_unknown(self):
        """Test refresh interval for unknown mode defaults to dashboard."""
        controller = DisplayController()

        interval = controller.get_refresh_interval("unknown_mode")
        # Should return fallback interval
        assert interval > 0
        assert isinstance(interval, int)

    def test_get_current_mode_uses_config(self):
        """Test that get_current_mode uses configured mode."""
        controller = DisplayController()

        # Regular day should use configured mode
        now = pendulum.parse("2024-06-15 12:00:00")
        mode = controller.get_current_mode(now)
        # Mode should be one of the valid modes
        assert mode in ["dashboard", "quote", "poetry", "wallpaper", "holiday"]
