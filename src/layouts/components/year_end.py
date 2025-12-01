"""Year-end summary component for dashboard layout."""

import datetime
import logging
from typing import Any

from PIL import ImageDraw

from src.config import BASE_DIR

from ...renderer.dashboard import DashboardRenderer
from ...renderer.icons.holiday import HolidayIcons
from ..utils.layout_helper import LayoutHelper

logger = logging.getLogger(__name__)


class YearEndSummaryComponent:
    """Handles rendering of the year-end summary screen."""

    # Layout constants
    TITLE_Y = 55
    TITLE_ICON_OFFSET = 337
    TITLE_ICON_SIZE = 40

    CONTRIB_Y = 140
    CONTRIB_LABEL_X = 180
    CONTRIB_VALUE_X = 470
    CONTRIB_VALUE_Y_OFFSET = 0

    LANG_Y = 210
    LANG_LABEL_X = 180
    LANG_ICONS_START_X = 450
    LANG_ICON_SPACING = 70
    LANG_ICON_SIZE = 30
    LANG_ICON_Y_OFFSET = 20

    STATS_Y = 300
    STATS_ICON_Y_OFFSET = 50
    STATS_ICON_SIZE = 24

    BOTTOM_Y_OFFSET = 60
    BOTTOM_ICON_OFFSET = 337
    BOTTOM_ICON_SIZE = 40

    # Icon paths
    ICONS_HOLIDAYS = f"{BASE_DIR}/resources/icons/holidays"
    ICONS_LANGUAGES = f"{BASE_DIR}/resources/icons/languages"
    ICONS_OCTICONS = f"{BASE_DIR}/resources/icons/octicons"

    # Language icon mapping
    LANG_ICONS = {
        "Python": "Python.png",
        "Go": "Go.png",
        "Java": "Java.png",
        "Rust": "Rust.png",
        "PHP": "PHP.png",
        "TypeScript": "TypeScript.png",
        "JavaScript": "JavaScript.png",
    }

    def __init__(self, renderer: DashboardRenderer):
        self.renderer = renderer
        self.layout = LayoutHelper(use_grayscale=False)
        self.icons = HolidayIcons()

    def draw(
        self, draw: ImageDraw.ImageDraw, width: int, height: int, summary_data: dict[str, Any]
    ) -> None:
        """Draw year-end summary (displayed on Dec 31st).

        Args:
            draw: PIL ImageDraw object
            width: Canvas width
            height: Canvas height
            summary_data: Year-end summary statistics
        """
        year = datetime.datetime.now().year
        center_x = width // 2

        # Draw all sections
        self._draw_title(draw, center_x, year)
        self._draw_contributions(draw, summary_data)
        self._draw_languages(draw, summary_data)
        self._draw_statistics(draw, width, summary_data)
        self._draw_bottom_message(draw, center_x, width, height, year)

    def _draw_title(self, draw: ImageDraw.ImageDraw, center_x: int, year: int) -> None:
        """Draw title with decorative icons."""
        title = f"{year} Year in Review"
        self.renderer.draw_centered_text(
            draw, center_x, self.TITLE_Y, title, font=self.renderer.font_l, align_y_center=True
        )

        # Left icon (satellite)
        self.icons.draw_image_icon(
            draw,
            center_x - self.TITLE_ICON_OFFSET,
            self.TITLE_Y,
            f"{self.ICONS_HOLIDAYS}/satellite.png",
            size=self.TITLE_ICON_SIZE,
        )

        # Right icon (astronaut)
        self.icons.draw_image_icon(
            draw,
            center_x + self.TITLE_ICON_OFFSET,
            self.TITLE_Y,
            f"{self.ICONS_HOLIDAYS}/astronaut.png",
            size=self.TITLE_ICON_SIZE,
        )

    def _draw_contributions(self, draw: ImageDraw.ImageDraw, data: dict[str, Any]) -> None:
        """Draw total contributions row."""
        total = data.get("total_contributions", data.get("total", 0))

        self.renderer.draw_text(
            draw,
            self.CONTRIB_LABEL_X,
            self.CONTRIB_Y,
            "Total Contributions",
            font=self.renderer.font_m,
        )
        self.renderer.draw_text(
            draw,
            self.CONTRIB_VALUE_X,
            self.CONTRIB_Y + self.CONTRIB_VALUE_Y_OFFSET,
            str(total),
            font=self.renderer.font_m,
        )

    def _draw_languages(self, draw: ImageDraw.ImageDraw, data: dict[str, Any]) -> None:
        """Draw top 3 languages row."""
        top_languages = data.get("top_languages", [])[:3]

        self.renderer.draw_text(
            draw, self.LANG_LABEL_X, self.LANG_Y, "Top 3 Languages", font=self.renderer.font_m
        )

        # Draw language icons
        for i, lang in enumerate(top_languages):
            icon_name = self.LANG_ICONS.get(lang)
            if not icon_name:
                continue

            x = self.LANG_ICONS_START_X + (i * self.LANG_ICON_SPACING)
            self.icons.draw_image_icon(
                draw,
                x,
                self.LANG_Y + self.LANG_ICON_Y_OFFSET,
                f"{self.ICONS_LANGUAGES}/{icon_name}",
                size=self.LANG_ICON_SIZE,
            )

    def _draw_statistics(self, draw: ImageDraw.ImageDraw, width: int, data: dict[str, Any]) -> None:
        """Draw bottom statistics row with icons."""
        stats_config = [
            (data.get("total_issues", 0), "issue-opened.png"),
            (data.get("total_prs", 0), "git-pull-request.png"),
            (data.get("total_stars", 0), "star.png"),
            (data.get("total_commits", 0), "git-commit.png"),
            (data.get("longest_streak", 0), "flame.png"),
            (data.get("total_reviews", 0), "code-review.png"),
            (data.get("most_productive_day", "N/A"), "pulse.png"),
        ]

        num_stats = len(stats_config)
        stat_spacing = width // (num_stats + 1)
        stats_icon_y = self.STATS_Y + self.STATS_ICON_Y_OFFSET

        for i, (value, icon_file) in enumerate(stats_config):
            x = stat_spacing * (i + 1)

            # Draw value
            value_str = str(value) if not isinstance(value, str) else value
            font = self.renderer.font_m if len(value_str) <= 3 else self.renderer.font_s
            self.renderer.draw_centered_text(
                draw, x, self.STATS_Y, value_str, font=font, align_y_center=True
            )

            # Draw icon
            self.icons.draw_image_icon(
                draw,
                x,
                stats_icon_y,
                f"{self.ICONS_OCTICONS}/{icon_file}",
                size=self.STATS_ICON_SIZE,
            )

    def _draw_bottom_message(
        self, draw: ImageDraw.ImageDraw, center_x: int, width: int, height: int, year: int
    ) -> None:
        """Draw bottom message with decorative icons."""
        bottom_y = height - self.BOTTOM_Y_OFFSET
        message = f'git commit -m "End of {year}"'

        self.renderer.draw_centered_text(
            draw, center_x, bottom_y, message, font=self.renderer.font_m, align_y_center=True
        )

        # Left icon (starship)
        self.icons.draw_image_icon(
            draw,
            center_x - self.BOTTOM_ICON_OFFSET,
            bottom_y,
            f"{self.ICONS_HOLIDAYS}/starship.png",
            size=self.BOTTOM_ICON_SIZE,
        )

        # Right icon (radar, flipped)
        self.icons.draw_image_icon(
            draw,
            center_x + self.BOTTOM_ICON_OFFSET,
            bottom_y,
            f"{self.ICONS_HOLIDAYS}/radar.png",
            size=self.BOTTOM_ICON_SIZE,
            flip_horizontal=True,
        )
