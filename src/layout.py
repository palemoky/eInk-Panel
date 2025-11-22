# src/layout.py
from PIL import Image, ImageDraw
import datetime
from .config import Config
from .renderer import Renderer
from .holiday import HolidayManager


class DashboardLayout:
    def __init__(self):
        self.renderer = Renderer()
        self.holiday_manager = HolidayManager()

        # === 布局常量定义 ===
        # 顶部区域
        self.TOP_Y = 15
        self.LINE_TOP_Y = 110

        # 列表区域
        self.LIST_HEADER_Y = 125
        self.LIST_START_Y = 165
        self.LINE_H = 40
        self.LINE_BOTTOM_Y = 365

        # 底部区域
        self.FOOTER_CENTER_Y = 410
        self.FOOTER_LABEL_Y = 445

        # 列表列配置 (X坐标, 最大宽度)
        self.COLS = [
            {"x": 40, "max_w": 260},  # Column 1
            {"x": 320, "max_w": 220},  # Column 2
            {"x": 560, "max_w": 220},  # Column 3
        ]

        # 列表显示最大行数
        self.MAX_LIST_LINES = 5
        
        # 天气图标配置
        self.WEATHER_ICON_OFFSET_X = -35  # 图标相对中心点的X偏移
        self.WEATHER_ICON_SIZE = 20       # 图标尺寸

    def create_image(self, width, height, data):
        """
        主入口：生成完整的仪表盘图片
        :param data: 包含所有显示数据的字典
        """
        # 1. 创建画布
        image = Image.new("1", (width, height), 255)
        draw = ImageDraw.Draw(image)

        # 0. 检查节日 (优先显示)
        holiday = self.holiday_manager.get_holiday()
        if holiday:
            self.renderer.draw_full_screen_message(
                draw, 
                width, 
                height, 
                holiday["title"], 
                holiday["message"], 
                holiday.get("icon")
            )
            return image

        # 0.5 检查年终总结 (12月31日)
        if data.get("is_year_end") and data.get("github_year_summary"):
            self._draw_year_end_summary(draw, width, height, data["github_year_summary"])
            return image

        # 2. 提取数据
        now = datetime.datetime.now()
        weather = data.get("weather", {})
        commits = data.get("github_commits", 0)
        vps_data = data.get("vps_usage", 0)
        btc_data = data.get("btc_price", {})
        week_prog = data.get("week_progress", 0)
        douban = data.get("douban", {"book": 0, "movie": 0, "music": 0})

        # 3. 绘制三大区域
        self._draw_header(draw, width, now, weather)
        self._draw_lists(draw)
        self._draw_footer(draw, width, commits, vps_data, btc_data, week_prog, douban)

        return image

    # ... (省略 _draw_header 和 _draw_lists，保持不变) ...

    def _draw_footer(self, draw, width, commits, vps_data, btc_data, week_prog, douban):
        """
        绘制底部区域：支持动态 Slot 分布
        """
        r = self.renderer

        # 构建 BTC 字符串
        btc_val = f"${btc_data['usd']}"
        btc_label = f"BTC ({btc_data['usd_24h_change']:.1f}%)"

        # 构建 GitHub 标签
        mode = Config.GITHUB_STATS_MODE.lower()
        if mode == "year":
            commit_label = f"Commits ({datetime.datetime.now().year})"
        elif mode == "month":
            commit_label = "Commits (Mo)"
        else:
            commit_label = "Commits (Day)"

        # 定义底部组件
        footer_items = [
            {"label": "Weekly", "value": week_prog, "type": "ring"},
            {"label": commit_label, "value": str(commits), "type": "text"},
            {"label": btc_label, "value": btc_val, "type": "text"},
        ]

        # 如果有豆瓣数据，显示豆瓣；否则显示 VPS
        if Config.DOUBAN_ID and (douban["book"] > 0 or douban["movie"] > 0):
             # 简单显示书/影
             douban_val = f"B:{douban['book']} M:{douban['movie']}"
             footer_items.append({"label": "Douban (Year)", "value": douban_val, "type": "text_small"})
        else:
             footer_items.append({"label": "VPS Data", "value": vps_data, "type": "ring"})

        # 计算动态布局
        content_width = width - 40
        start_x = 20
        slot_width = content_width / len(footer_items)

        for i, item in enumerate(footer_items):
            center_x = int(start_x + (i * slot_width) + (slot_width / 2))

            # 绘制底部标签
            r.draw_centered_text(
                draw,
                center_x,
                self.FOOTER_LABEL_Y,
                item["label"],
                font=r.font_s,
                align_y_center=False,
            )

            # 绘制主要内容
            if item["type"] == "ring":
                radius = 32
                # 画圆环
                r.draw_progress_ring(
                    draw,
                    center_x,
                    self.FOOTER_CENTER_Y,
                    radius,
                    item["value"],
                    thickness=6,
                )
                # 画圆环中间百分比 (小字体)
                r.draw_centered_text(
                    draw,
                    center_x,
                    self.FOOTER_CENTER_Y,
                    f"{item['value']}%",
                    font=r.font_xs,
                    align_y_center=True,
                )
            elif item["type"] == "text_small":
                 r.draw_centered_text(
                    draw,
                    center_x,
                    self.FOOTER_CENTER_Y,
                    str(item["value"]),
                    font=r.font_m, # 使用中号字体
                    align_y_center=True,
                )
            else:
                # 画大数字
                r.draw_centered_text(
                    draw,
                    center_x,
                    self.FOOTER_CENTER_Y,
                    str(item["value"]),
                    font=r.font_l,
                    align_y_center=True,
                )

    def _draw_year_end_summary(self, draw, width, height, summary):
        """
        绘制年终总结 (12月31日显示)
        """
        r = self.renderer
        year = datetime.datetime.now().year
        
        # 标题
        r.draw_centered_text(draw, width // 2, 50, f"{year} Year in Review", font=r.font_l, align_y_center=False)
        
        # 核心数据
        center_y = height // 2
        
        # Total Commits
        r.draw_centered_text(draw, width // 2, center_y - 60, str(summary['total']), font=r.font_xl, align_y_center=True)
        r.draw_centered_text(draw, width // 2, center_y, "Total Contributions", font=r.font_m, align_y_center=True)
        
        # 详细数据 (Max / Avg)
        detail_y = center_y + 80
        detail_text = f"Max Day: {summary['max']}   |   Daily Avg: {summary['avg']}"
        r.draw_centered_text(draw, width // 2, detail_y, detail_text, font=r.font_s, align_y_center=True)
        
        # 底部祝福
        r.draw_centered_text(draw, width // 2, height - 40, "See you in next year!", font=r.font_s, align_y_center=True)

    def _limit_list_items(self, src_list, max_lines):
        """
        辅助函数：限制列表行数，超出显示 '...'
        """
        if len(src_list) > max_lines:
            return src_list[: max_lines - 1] + ["..."]
        return src_list
