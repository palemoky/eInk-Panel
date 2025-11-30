"""Header component for dashboard layout."""

import logging
from typing import Any

from PIL import ImageDraw

from ...config import Config
from ...renderer.dashboard import DashboardRenderer

logger = logging.getLogger(__name__)


class HeaderComponent:
    """Handles rendering of the dashboard header section."""

    def __init__(self, renderer: DashboardRenderer):
        self.renderer = renderer
        self.TOP_Y = 20
        self.LINE_TOP_Y = 100
        self.WEATHER_ICON_SIZE = 30

    def draw(
        self, draw: ImageDraw.ImageDraw, width: int, now: Any, weather: dict[str, Any]
    ) -> None:
        """Draw header section with dynamic slot distribution.

        Args:
            draw: PIL ImageDraw object
            width: Canvas width
            now: Current datetime
            weather: Weather data dictionary
        """
        # Define components to display
        header_items = [
            {"type": "weather", "data": weather},
            {"type": "date", "data": now},
            {"type": "greeting"},
            {"type": "time", "data": now},
        ]

        # Calculate dynamic layout parameters
        content_width = width - 20  # 10px padding on each side
        start_x = 10
        slot_width = content_width / len(header_items)

        # Draw each component
        for i, item in enumerate(header_items):
            center_x = int(start_x + (i * slot_width) + (slot_width / 2))
            self._draw_component(draw, center_x, self.TOP_Y, item)

        # Draw divider line in dark gray
        line_color = self.renderer.COLOR_DARK_GRAY if Config.hardware.use_grayscale else 0
        draw.line((30, self.LINE_TOP_Y, width - 30, self.LINE_TOP_Y), fill=line_color, width=2)

    def _draw_component(
        self, draw: ImageDraw.ImageDraw, center_x: int, top_y: int, item_data: dict[str, Any]
    ) -> None:
        """Draw individual header component."""
        r = self.renderer
        item_type = item_data["type"]

        match item_type:
            case "weather":
                data = item_data["data"]
                # Line 1: City and temperature
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y,
                    f"{Config.CITY_NAME} {data.get('temp', '--')}°",
                    font=r.font_m,
                    align_y_center=False,
                )

                # Line 2: Icon + description
                icon_y = top_y + 50
                w_main = data.get("icon", "")

                # Determine icon name
                icon_name = "cloud"
                if "Clear" in w_main or "Sun" in w_main:
                    icon_name = "sun"
                elif "Rain" in w_main or "Drizzle" in w_main:
                    icon_name = "rain"
                elif "Snow" in w_main:
                    icon_name = "snow"
                elif "Thunder" in w_main:
                    icon_name = "thunder"

                # Process description text
                desc = data.get("desc", "--")
                if desc == "Clouds":
                    desc = "Cloudy"
                if desc == "Thunderstorm":
                    desc = "Storm"

                # Calculate centering
                icon_size = self.WEATHER_ICON_SIZE
                try:
                    text_bbox = r.font_s.getbbox(desc)
                    text_width = text_bbox[2] - text_bbox[0]
                except Exception:
                    text_width = 40  # Fallback

                total_width = icon_size + 2 + text_width
                start_x = center_x - (total_width // 2)
                icon_x = start_x
                text_x = start_x + icon_size + 2

                r.draw_weather_icon(draw, icon_x, icon_y, icon_name, size=icon_size)
                draw.text((text_x, icon_y - 12), desc, font=r.font_s, fill=0)

            case "date":
                data = item_data["data"]
                weekday = data.strftime("%a")
                day = data.strftime("%d")
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y,
                    f"{weekday}, {day}",
                    font=r.font_date_big,
                    align_y_center=False,
                )

                month_year = data.strftime("%b %Y")
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y + 40,
                    month_year,
                    font=r.font_s,
                    align_y_center=False,
                )

            case "time":
                data = item_data["data"]
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y,
                    "Updated",
                    font=r.font_s,
                    align_y_center=False,
                )
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y + 35,
                    data.strftime("%H:%M"),
                    font=r.font_m,
                    align_y_center=False,
                )

            case "greeting":
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y,
                    Config.GREETING_LABEL,
                    font=r.font_m,
                    align_y_center=False,
                )
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y + 35,
                    Config.GREETING_TEXT,
                    font=r.font_m,
                    align_y_center=False,
                )

            case "custom":
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y,
                    item_data["label"],
                    font=r.font_s,
                    align_y_center=False,
                )
                r.draw_centered_text(
                    draw,
                    center_x,
                    top_y + 35,
                    item_data["value"],
                    font=r.font_value,
                    align_y_center=False,
                )
