"""Main entry point for the E-Ink Panel dashboard application.

Refactored to use modular components for better maintainability.
"""

import asyncio
import logging
import os
import signal
import sys
from typing import Any

import pendulum

# Try relative import first (for package mode)
try:
    from .config import Config, start_config_watcher, stop_config_watcher
    from .core import (
        DisplayController,
        QuietHours,
        TaskManager,
        TimeSlots,
    )
    from .core.data_fetcher import DataFetcher
    from .drivers.factory import get_driver
    from .layouts import DashboardLayout
    from .providers import Dashboard
    from .providers.hackernews import get_hackernews
    from .renderer.image_builder import ImageBuilder
    from .tasks.hackernews import hackernews_pagination_task
except ImportError:
    # If relative import fails, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import Config, start_config_watcher, stop_config_watcher
    from src.core import (
        DisplayController,
        QuietHours,
        TaskManager,
        TimeSlots,
    )
    from src.core.data_fetcher import DataFetcher
    from src.drivers.factory import get_driver
    from src.layouts import DashboardLayout
    from src.providers import Dashboard
    from src.providers.hackernews import get_hackernews
    from src.renderer.image_builder import ImageBuilder
    from src.tasks.hackernews import hackernews_pagination_task

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Global variable for signal handling
_driver = None


def signal_handler(signum: int, frame: Any) -> None:
    """Handle SIGTERM/SIGINT signals for graceful shutdown."""
    logger.info(f"\\n🛑 Received signal {signum}, shutting down gracefully...")
    if _driver:
        try:
            logger.info("Putting display to sleep...")
            _driver.sleep()
            logger.info("✅ Display sleep successful")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def ensure_fonts() -> None:
    """Ensure required fonts are available, downloading if necessary.

    This function is called on application startup to ensure the WaveShare font
    (required for dashboard, quote, and other modes) is available. If download
    fails, the application will fall back to PIL's default font.
    """
    try:
        from .utils.fonts import FontManager

        logger.info("🔤 Checking font availability...")

        # Download WaveShare font (required for all modes)
        font_path = FontManager.get_font_path("WaveShare.ttc", url=FontManager.WAVESHARE_URL)

        if os.path.exists(font_path):
            logger.info(f"✅ WaveShare font available at {font_path}")
        else:
            logger.warning(
                "⚠️  WaveShare font not found. Application will use default fonts. "
                "For better display quality, ensure fonts are available in the fonts/ directory."
            )

    except Exception as e:
        logger.warning(
            f"⚠️  Font initialization failed: {e}. "
            "Application will use default fonts with reduced quality."
        )


async def update_display(epd, image: Any, config_changed: asyncio.Event) -> None:
    """Update the E-Paper display with a new image.

    Args:
        epd: E-Paper Display driver instance
        image: PIL Image to display
        config_changed: Event that signals configuration has changed
    """
    try:
        # Check if config changed during image generation
        if config_changed.is_set():
            logger.info("⚠️  Config changed during image generation, skipping display update")
            config_changed.clear()
            return

        # Initialize display
        epd.init()
        logger.info("🖼️  Updating display...")

        # Display image
        epd.display(image)
        logger.info("✅ Display updated successfully")

        # Put display to sleep to save power
        epd.sleep()

    except Exception as e:
        logger.error(f"Failed to update display: {e}")
        raise


async def handle_quiet_hours(quiet: QuietHours, config_changed: asyncio.Event) -> bool:
    """Handle quiet hours by sleeping if currently in quiet period.

    Args:
        quiet: QuietHours instance
        config_changed: Event that signals configuration has changed

    Returns:
        True if we slept during quiet hours, False otherwise
    """
    is_quiet, sleep_seconds = quiet.check()

    if is_quiet:
        logger.info(f"😴 Quiet hours active, sleeping for {sleep_seconds}s...")
        try:
            await asyncio.wait_for(config_changed.wait(), timeout=sleep_seconds)
            logger.info("⚙️  Config changed during quiet hours, resuming...")
            config_changed.clear()
        except asyncio.TimeoutError:
            logger.info("⏰ Quiet hours ended, resuming...")
        return True

    return False


async def wait_for_refresh(interval: int, config_changed: asyncio.Event) -> bool:
    """Wait for refresh interval or config change.

    Args:
        interval: Refresh interval in seconds
        config_changed: Event that signals configuration has changed

    Returns:
        True if config changed, False if timeout
    """
    logger.info(f"⏳ Waiting {interval}s until next refresh...")
    try:
        await asyncio.wait_for(config_changed.wait(), timeout=interval)
        logger.info("⚙️  Config changed, triggering immediate refresh...")
        config_changed.clear()
        return True
    except asyncio.TimeoutError:
        return False


def _log_startup_info() -> None:
    """Log startup information about configuration."""
    logger.info("Starting E-Ink Panel Dashboard...")
    logger.info(f"  Display mode: {Config.display.mode}")
    logger.info(f"  Timezone: {Config.hardware.timezone}")
    logger.info(
        f"  Quiet hours: {Config.hardware.quiet_start_hour}:00 - {Config.hardware.quiet_end_hour}:00"
    )
    logger.info(f"  Grayscale: {Config.hardware.use_grayscale}")


async def main():
    """Main application loop."""
    global _driver

    # Validate configuration
    Config.validate_required()
    _log_startup_info()

    # Ensure fonts are available (download if necessary)
    ensure_fonts()

    # Initialize components
    epd = get_driver()
    _driver = epd  # For signal handler
    layout = DashboardLayout()
    controller = DisplayController()
    quiet = QuietHours(
        Config.hardware.quiet_start_hour, Config.hardware.quiet_end_hour, Config.hardware.timezone
    )

    # Configuration change event
    config_changed = asyncio.Event()

    def on_config_reload():
        """Callback when config is reloaded."""
        logger.info("📢 Config reloaded, triggering refresh...")
        config_changed.set()

    # Start config watcher
    start_config_watcher()

    # Initialize time slots for TODO display
    # HackerNews will show during non-TODO hours
    todo_slots = TimeSlots(Config.display.todo_time_slots)

    try:
        async with Dashboard() as dm, TaskManager() as task_mgr:
            fetcher = DataFetcher(dm)
            builder = ImageBuilder(epd.width, epd.height)

            # Reset HackerNews pagination on startup only if in HackerNews time slot
            now = pendulum.now(Config.hardware.timezone)
            show_hn = not todo_slots.contains_hour(now.hour)
            if show_hn:
                await get_hackernews(dm.client, reset_to_first=True)
                logger.info("🔄 Reset HackerNews pagination on startup")

            # Main loop
            while True:
                # Check quiet hours
                if await handle_quiet_hours(quiet, config_changed):
                    continue

                # Determine display mode
                now = pendulum.now(Config.hardware.timezone)
                mode = controller.get_current_mode(now)

                # Manage HackerNews pagination task
                # Show HN during non-TODO hours in dashboard mode
                show_hn = mode == "dashboard" and not todo_slots.contains_hour(now.hour)

                if show_hn:
                    if not await task_mgr.is_running("hackernews"):
                        await task_mgr.start(
                            "hackernews", hackernews_pagination_task, epd, layout, dm
                        )
                else:
                    if await task_mgr.is_running("hackernews"):
                        await task_mgr.stop("hackernews")

                # Fetch data
                try:
                    data = await fetcher.fetch(mode)
                except Exception as e:
                    logger.error(f"Failed to fetch data: {e}")
                    continue

                # Generate image
                try:
                    image = builder.build(mode, data, layout)
                except Exception as e:
                    logger.error(f"Failed to generate image: {e}")
                    continue

                # Update display
                await update_display(epd, image, config_changed)

                # Wait for next refresh
                interval = controller.get_refresh_interval(mode)
                await wait_for_refresh(interval, config_changed)

    except KeyboardInterrupt:
        logger.info("\\n👋 Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        stop_config_watcher()
        if _driver:
            try:
                _driver.sleep()
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(main())
