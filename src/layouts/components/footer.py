"""Footer component for dashboard layout."""

import logging
from typing import Any

from PIL import ImageDraw

from ...renderer.dashboard import DashboardRenderer

logger = logging.getLogger(__name__)


class FooterComponent:
    """Handles rendering of the dashboard footer section."""

    def __init__(self, renderer: DashboardRenderer):
        self.renderer = renderer
        self.FOOTER_CENTER_Y = 410
        self.FOOTER_LABEL_Y = 445

    def draw(
        self,
        draw: ImageDraw.ImageDraw,
        width: int,
        commits: int | dict,
        vps_data: int,
        btc_data: dict[str, Any],
        week_prog: int,
    ) -> None:
        """Draw the footer section: supports dynamic slot distribution.

        Args:
            draw: PIL ImageDraw object
            width: Canvas width
            commits: GitHub commit count
            vps_data: VPS usage data
            btc_data: Bitcoin price data
            week_prog: Week progress percentage
        """
        r = self.renderer

        # Construct BTC string
        btc_val = f"${btc_data.get('usd', 0):,}"
        change = btc_data.get("usd_24h_change", 0.0)
        btc_label = f"BTC ({change:+.1f}%)"

        # Define footer components
        footer_items = [
            {"label": "Weekly", "value": week_prog, "type": "ring"},
            {"label": "Commits", "value": commits, "type": "cross"},
            {"label": btc_label, "value": btc_val, "type": "text"},
            {"label": "VPS Data", "value": vps_data, "type": "ring"},
        ]

        # Calculate dynamic layout parameters
        content_width = width - 40
        start_x = 20
        slot_width = content_width / len(footer_items)

        # Loop to draw components
        for i, item in enumerate(footer_items):
            center_x = int(start_x + (i * slot_width) + (slot_width / 2))

            # Draw label
            r.draw_centered_text(
                draw,
                center_x,
                self.FOOTER_LABEL_Y,
                item["label"],
                font=r.font_s,
                align_y_center=False,
            )

            # Draw value based on type
            if item["type"] == "ring":
                self._draw_ring_item(draw, center_x, item["value"])
            elif item["type"] == "cross":
                self._draw_cross_item(draw, center_x, item["value"])
            elif item["type"] == "text":
                self._draw_text_item(draw, center_x, str(item["value"]))
            else:
                logger.warning(f"Unknown footer item type: {item['type']}")
                self._draw_text_item(draw, center_x, str(item["value"]))

    def _draw_ring_item(self, draw: ImageDraw.ImageDraw, center_x: int, value: int) -> None:
        """Draw a ring progress item."""
        r = self.renderer
        radius = 32
        r.draw_progress_ring(
            draw,
            center_x,
            self.FOOTER_CENTER_Y,
            radius,
            value,
            thickness=6,
        )
        r.draw_centered_text(
            draw,
            center_x,
            self.FOOTER_CENTER_Y,
            f"{value}%",
            font=r.font_xs,
            align_y_center=True,
        )

    def _draw_text_item(self, draw: ImageDraw.ImageDraw, center_x: int, value: str) -> None:
        """Draw a simple text item."""
        r = self.renderer
        r.draw_centered_text(
            draw,
            center_x,
            self.FOOTER_CENTER_Y,
            value,
            font=r.font_date_big,
            align_y_center=True,
        )

    def _draw_cross_item(self, draw: ImageDraw.ImageDraw, center_x: int, value: Any) -> None:
        """Draw a cross layout item (typically for GitHub stats)."""
        r = self.renderer

        # Special handling for GitHub stats (dictionary)
        if (
            isinstance(value, dict)
            and "day" in value
            and "week" in value
            and "month" in value
            and "year" in value
        ):
            offset_x = 25
            offset_y = 15

            # Top-left: Day
            r.draw_centered_text(
                draw,
                center_x - offset_x,
                self.FOOTER_CENTER_Y - offset_y,
                str(value["day"]),
                font=r.font_commits,
                align_y_center=True,
            )

            # Top-right: Week
            r.draw_centered_text(
                draw,
                center_x + offset_x,
                self.FOOTER_CENTER_Y - offset_y,
                str(value["week"]),
                font=r.font_commits,
                align_y_center=True,
            )

            # Bottom-left: Month
            r.draw_centered_text(
                draw,
                center_x - offset_x,
                self.FOOTER_CENTER_Y + offset_y,
                str(value["month"]),
                font=r.font_commits,
                align_y_center=True,
            )

            # Bottom-right: Year
            r.draw_centered_text(
                draw,
                center_x + offset_x,
                self.FOOTER_CENTER_Y + offset_y,
                str(value["year"]),
                font=r.font_commits,
                align_y_center=True,
            )

            # Draw cross lines
            draw.line(
                (
                    center_x,
                    self.FOOTER_CENTER_Y - offset_y - 10,
                    center_x,
                    self.FOOTER_CENTER_Y + offset_y + 10,
                ),
                fill=0,
                width=1,
            )
            draw.line(
                (
                    center_x - offset_x - 15,
                    self.FOOTER_CENTER_Y,
                    center_x + offset_x + 15,
                    self.FOOTER_CENTER_Y,
                ),
                fill=0,
                width=1,
            )
        else:
            # Fallback to text if not a valid dict
            self._draw_text_item(draw, center_x, str(value))
