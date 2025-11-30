"""Dashboard renderer - Main coordinator.

Coordinates text, shapes, and icon rendering using modular components.
"""

from PIL import ImageFont

from ..config import Config
from .icons import HolidayIcons, WeatherIcons
from .shapes import ShapeRenderer
from .text import TextRenderer


class DashboardRenderer:
    """Handles all drawing operations for the dashboard.

    Coordinates text rendering, shape drawing, and icon rendering
    using modular components for better organization.
    """

    # Grayscale color constants
    COLOR_BLACK = 0
    COLOR_DARK_GRAY = 128
    COLOR_LIGHT_GRAY = 192
    COLOR_WHITE = 255

    def __init__(self):
        self._load_fonts()

        # Initialize component renderers
        self.text = TextRenderer()
        self.shapes = ShapeRenderer()
        self.weather_icons = WeatherIcons()
        self.holiday_icons = HolidayIcons()

    def _load_fonts(self):
        """Load fonts for rendering."""
        try:
            fp = Config.FONT_PATH
            self.font_xs = ImageFont.truetype(fp, 18)
            self.font_s = ImageFont.truetype(fp, 24)
            self.font_m = ImageFont.truetype(fp, 28)
            self.font_value = ImageFont.truetype(fp, 32)
            self.font_date_big = ImageFont.truetype(fp, 34)
            self.font_date_small = ImageFont.truetype(fp, 24)
            self.font_commits = ImageFont.truetype(fp, 20)
            self.font_l = ImageFont.truetype(fp, 48)
            self.font_xl = ImageFont.truetype(fp, 60)
        except IOError:
            self.font_s = self.font_m = self.font_l = self.font_xl = ImageFont.load_default()
            self.font_xs = self.font_value = self.font_date_big = self.font_date_small = self.font_s

    # Convenience methods that delegate to component renderers

    def draw_text(self, draw, x, y, text, font, fill=0, anchor=None):
        """Draw text (delegates to TextRenderer)."""
        self.text.draw_text(draw, x, y, text, font, fill, anchor)

    def draw_centered_text(self, draw, x, y, text, font, fill=0, align_y_center=True):
        """Draw centered text (delegates to TextRenderer)."""
        self.text.draw_centered_text(draw, x, y, text, font, fill, align_y_center)

    def draw_truncated_text(self, draw, x, y, text, font, max_width, fill=0):
        """Draw truncated text (delegates to TextRenderer)."""
        self.text.draw_truncated_text(draw, x, y, text, font, max_width, fill)

    def draw_progress_ring(self, draw, x, y, radius, percent, thickness=5):
        """Draw progress ring (delegates to ShapeRenderer)."""
        self.shapes.draw_progress_ring(
            draw, x, y, radius, percent, thickness, use_grayscale=Config.hardware.use_grayscale
        )

    def draw_weather_icon(self, draw, x, y, icon_name, size=30):
        """Draw weather icon (delegates to WeatherIcons)."""
        from ..config import BASE_DIR

        icons_dir = BASE_DIR / "resources" / "icons" / "weather"
        return self.weather_icons.draw_weather_icon(draw, x, y, icon_name, size, icons_dir)

    def draw_full_screen_message(self, draw, width, height, title, message, icon_type=None):
        """Draw full screen message (delegates to HolidayIcons)."""
        self.holiday_icons.draw_full_screen_message(
            draw, width, height, title, message, icon_type, self.font_l, self.font_m
        )
