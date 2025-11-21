from PIL import ImageDraw, ImageFont
import math
from .config import Config


class Renderer:
    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        try:
            fp = Config.FONT_PATH
            self.font_xs = ImageFont.truetype(fp, 18)
            self.font_s = ImageFont.truetype(fp, 24)
            self.font_m = ImageFont.truetype(fp, 28)
            self.font_time = ImageFont.truetype(fp, 32)
            self.font_date_big = ImageFont.truetype(fp, 40)
            self.font_date_small = ImageFont.truetype(fp, 24)
            self.font_l = ImageFont.truetype(fp, 48)
        except IOError:
            self.font_s = self.font_m = self.font_l = ImageFont.load_default()
            # Fallback mapping
            self.font_xs = self.font_time = self.font_date_big = (
                self.font_date_small
            ) = self.font_s

    def draw_centered_text(self, draw, x, y, text, font, fill=0, align_y_center=True):
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
        except AttributeError:
            w, h = draw.textsize(text, font=font)

        y_offset = (h // 2 + 3) if align_y_center else 0
        draw.text((x - w // 2, y - y_offset), text, font=font, fill=fill)

    def draw_truncated_text(self, draw, x, y, text, font, max_width, fill=0):
        def get_w(t):
            try:
                return draw.textlength(t, font=font)
            except AttributeError:
                w, _ = draw.textsize(t, font=font)
                return w

        if get_w(text) <= max_width:
            draw.text((x, y), text, font=font, fill=fill)
            return

        ellipsis = "..."
        for i in range(len(text), 0, -1):
            temp = text[:i]
            if get_w(temp) + get_w(ellipsis) <= max_width:
                draw.text((x, y), temp + ellipsis, font=font, fill=fill)
                return

    def draw_progress_ring(self, draw, x, y, radius, percent, thickness=5):
        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.ellipse(bbox, outline=0, width=1)

        start_angle = -90
        # Ensure percent is int/float
        try:
            p = float(percent)
        except ValueError:
            p = 0

        end_angle = -90 + (360 * (p / 100.0))
        if p > 0:
            draw.pieslice(bbox, start=start_angle, end=end_angle, fill=0)

        inner_r = radius - thickness
        draw.ellipse(
            (x - inner_r, y - inner_r, x + inner_r, y + inner_r), fill=255, outline=0
        )

    # --- Icons (Scaled) ---

    def draw_icon_sun(self, draw, x, y, size=20):
        r = size // 3
        draw.ellipse((x - r, y - r, x + r, y + r), outline=0, width=2)
        for i in range(0, 360, 45):
            angle = math.radians(i)
            # Scale ray length based on size
            ray_start = r + (size * 0.125)
            ray_end = r + (size * 0.25)
            x1 = x + math.cos(angle) * ray_start
            y1 = y + math.sin(angle) * ray_start
            x2 = x + math.cos(angle) * ray_end
            y2 = y + math.sin(angle) * ray_end
            draw.line((x1, y1, x2, y2), fill=0, width=2)

    def draw_icon_cloud(self, draw, x, y, size=20):
        # Base scale relative to original hardcoded 40px
        s = size / 40.0

        # Adjust center Y slightly down
        y = y + (5 * s)

        # Relative coordinates scaled by s
        # Left circle
        draw.ellipse(
            (x - 20 * s, y - 5 * s, x, y + 15 * s),
            fill=255,
            outline=0,
            width=max(1, int(2 * s)),
        )
        # Right circle
        draw.ellipse(
            (x, y - 5 * s, x + 20 * s, y + 15 * s),
            fill=255,
            outline=0,
            width=max(1, int(2 * s)),
        )
        # Top circle
        draw.ellipse(
            (x - 10 * s, y - 15 * s, x + 10 * s, y + 5 * s),
            fill=255,
            outline=0,
            width=max(1, int(2 * s)),
        )

        # Cover bottom lines
        draw.rectangle((x - 10 * s, y, x + 10 * s, y + 10 * s), fill=255)

    def draw_icon_rain(self, draw, x, y, size=20):
        self.draw_icon_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (15 * s)

        line_len = 10 * s
        offset = 8 * s

        draw.line(
            (x - offset, y_base + 5 * s, x - offset, y_base + 5 * s + line_len),
            fill=0,
            width=max(1, int(2 * s)),
        )
        draw.line(
            (x, y_base + 5 * s, x, y_base + 5 * s + line_len),
            fill=0,
            width=max(1, int(2 * s)),
        )
        draw.line(
            (x + offset, y_base + 5 * s, x + offset, y_base + 5 * s + line_len),
            fill=0,
            width=max(1, int(2 * s)),
        )

    def draw_icon_snow(self, draw, x, y, size=20):
        self.draw_icon_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (15 * s)
        r_snow = 2 * s
        
        draw.ellipse(
            (x - 12 * s, y_base + 5 * s, x - 12 * s + r_snow * 2, y_base + 5 * s + r_snow * 2), 
            fill=0
        ) 
        draw.ellipse(
            (x - 2 * s, y_base + 8 * s, x - 2 * s + r_snow * 2, y_base + 8 * s + r_snow * 2), 
            fill=0
        ) 
        draw.ellipse(
            (x + 8 * s, y_base + 5 * s, x + 8 * s + r_snow * 2, y_base + 5 * s + r_snow * 2), 
            fill=0
        )

    def draw_icon_thunder(self, draw, x, y, size=20):
        self.draw_icon_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (10 * s)
        
        points = [
            (x + 2 * s, y_base),  
            (x - 5 * s, y_base + 10 * s),  
            (x, y_base + 10 * s),  
            (x - 3 * s, y_base + 20 * s),  
        ]
        draw.line(points, fill=0, width=max(1, int(2 * s)))
