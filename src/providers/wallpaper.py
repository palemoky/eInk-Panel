"""Wallpaper manager for loading and displaying wallpaper images.

Loads wallpaper images from resources/wallpapers directory.
Supports random selection or specific wallpaper by name.
"""

import logging
import random
from pathlib import Path

from PIL import Image

from ..config import BASE_DIR

logger = logging.getLogger(__name__)


class WallpaperManager:
    """Manager for loading and displaying wallpaper images."""

    def __init__(self):
        """Initialize wallpaper manager."""
        self.wallpapers_dir = BASE_DIR / "resources" / "wallpapers"
        self.wallpapers_dir.mkdir(parents=True, exist_ok=True)

    def get_available_wallpapers(self) -> list[Path]:
        """Get list of available wallpaper files.

        Returns:
            List of wallpaper file paths
        """
        # Support common image formats
        extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]
        wallpapers = []

        for ext in extensions:
            wallpapers.extend(self.wallpapers_dir.glob(ext))
            # Also check uppercase extensions
            wallpapers.extend(self.wallpapers_dir.glob(ext.upper()))

        return sorted(wallpapers)

    def create_wallpaper(
        self, width: int, height: int, wallpaper_name: str | None = None
    ) -> Image.Image:
        """Create wallpaper image for display.

        Args:
            width: Display width in pixels
            height: Display height in pixels
            wallpaper_name: Specific wallpaper name (without extension) or None for random

        Returns:
            PIL Image object ready for display

        Raises:
            FileNotFoundError: If no wallpapers found or specified wallpaper doesn't exist
        """
        available_wallpapers = self.get_available_wallpapers()

        if not available_wallpapers:
            logger.error(f"No wallpapers found in {self.wallpapers_dir}")
            # Create a blank image as fallback
            return Image.new("L", (width, height), 255)

        # Select wallpaper
        if wallpaper_name:
            # Find wallpaper by name (without extension)
            selected = None
            for wp in available_wallpapers:
                if wp.stem == wallpaper_name:
                    selected = wp
                    break

            if not selected:
                logger.warning(
                    f"Wallpaper '{wallpaper_name}' not found, using random. "
                    f"Available: {[wp.stem for wp in available_wallpapers]}"
                )
                selected = random.choice(available_wallpapers)
        else:
            # Random selection
            selected = random.choice(available_wallpapers)

        logger.info(f"Loading wallpaper: {selected.name}")

        try:
            # Load and process image
            image = Image.open(selected)

            # Convert to grayscale for e-ink display
            if image.mode != "L":
                image = image.convert("L")

            # Resize to fit display while maintaining aspect ratio
            image.thumbnail((width, height), Image.Resampling.LANCZOS)

            # Create final image with correct size (center the wallpaper)
            final_image = Image.new("L", (width, height), 255)
            offset_x = (width - image.width) // 2
            offset_y = (height - image.height) // 2
            final_image.paste(image, (offset_x, offset_y))

            logger.info(
                f"Wallpaper loaded successfully: {selected.name} "
                f"(original: {image.width}x{image.height}, display: {width}x{height})"
            )

            return final_image

        except Exception as e:
            logger.error(f"Failed to load wallpaper {selected}: {e}")
            # Return blank image as fallback
            return Image.new("L", (width, height), 255)
