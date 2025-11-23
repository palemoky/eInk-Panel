"""
壁纸管理器 - 用于显示艺术壁纸
支持太空主题、自然风景等
"""

import random

from PIL import Image, ImageDraw

from .renderer import Renderer


class WallpaperManager:
    def __init__(self):
        self.renderer = Renderer()

    def get_wallpaper_list(self):
        """获取可用的壁纸列表"""
        return [
            # 太空主题
            "solar_system",
            "starship",
            "earth_rise",
            "saturn_rings",
            "galaxy",
            "moon_landing",
            "mars_landscape",
            "nebula",
            # 自然主题
            "snow_mountain",
            "cherry_blossom",
            "sunset_beach",
            "forest_path",
            "northern_lights",
            # 温馨主题
            "family_home",
            "couple_love",
            "coffee_time",
            "reading_room",
            "rainy_window",
            # 动植物主题
            "cat_nap",
            "dog_play",
            "bird_tree",
            "butterfly_garden",
            "whale_ocean",
            "panda_bamboo",
            "flower_meadow",
            "cactus_desert",
        ]

    def create_wallpaper(self, width: int, height: int, wallpaper_name: str = None) -> Image.Image:
        """
        创建壁纸图像

        Args:
            width: 图像宽度
            height: 图像高度
            wallpaper_name: 壁纸名称，如果为 None 则随机选择

        Returns:
            PIL Image 对象
        """
        if wallpaper_name is None:
            wallpaper_name = random.choice(self.get_wallpaper_list())

        # 创建画布
        image = Image.new("1", (width, height), 255)  # 白色背景
        draw = ImageDraw.Draw(image)

        # 根据壁纸名称绘制
        match wallpaper_name:
            # 太空主题
            case "solar_system":
                self._draw_solar_system(draw, width, height)
            case "starship":
                self._draw_starship(draw, width, height)
            case "earth_rise":
                self._draw_earth_rise(draw, width, height)
            case "saturn_rings":
                self._draw_saturn_rings(draw, width, height)
            case "galaxy":
                self._draw_galaxy(draw, width, height)
            case "moon_landing":
                self._draw_moon_landing(draw, width, height)
            case "mars_landscape":
                self._draw_mars_landscape(draw, width, height)
            case "nebula":
                self._draw_nebula(draw, width, height)
            # 自然主题
            case "snow_mountain":
                self._draw_snow_mountain(draw, width, height)
            case "cherry_blossom":
                self._draw_cherry_blossom(draw, width, height)
            case "sunset_beach":
                self._draw_sunset_beach(draw, width, height)
            case "forest_path":
                self._draw_forest_path(draw, width, height)
            case "northern_lights":
                self._draw_northern_lights(draw, width, height)
            # 温馨主题
            case "family_home":
                self._draw_family_home(draw, width, height)
            case "couple_love":
                self._draw_couple_love(draw, width, height)
            case "coffee_time":
                self._draw_coffee_time(draw, width, height)
            case "reading_room":
                self._draw_reading_room(draw, width, height)
            case "rainy_window":
                self._draw_rainy_window(draw, width, height)
            # 动植物主题
            case "cat_nap":
                self._draw_cat_nap(draw, width, height)
            case "dog_play":
                self._draw_dog_play(draw, width, height)
            case "bird_tree":
                self._draw_bird_tree(draw, width, height)
            case "butterfly_garden":
                self._draw_butterfly_garden(draw, width, height)
            case "whale_ocean":
                self._draw_whale_ocean(draw, width, height)
            case "panda_bamboo":
                self._draw_panda_bamboo(draw, width, height)
            case "flower_meadow":
                self._draw_flower_meadow(draw, width, height)
            case "cactus_desert":
                self._draw_cactus_desert(draw, width, height)
            case _:
                self._draw_solar_system(draw, width, height)

        return image

    def _draw_solar_system(self, draw, width, height):
        """绘制太阳系壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Solar System", r.font_l)

        # 太阳（中心）
        sun_x, sun_y = 100, center_y
        draw.ellipse((sun_x - 30, sun_y - 30, sun_x + 30, sun_y + 30), fill=0)
        r.draw_centered_text(draw, sun_x, sun_y + 50, "Sun", r.font_xs)

        # 行星轨道和行星
        planets = [
            {"name": "Mercury", "distance": 80, "size": 8},
            {"name": "Venus", "distance": 120, "size": 12},
            {"name": "Earth", "distance": 170, "size": 13},
            {"name": "Mars", "distance": 220, "size": 10},
            {"name": "Jupiter", "distance": 320, "size": 25},
            {"name": "Saturn", "distance": 420, "size": 22},
            {"name": "Uranus", "distance": 520, "size": 18},
            {"name": "Neptune", "distance": 620, "size": 17},
        ]

        for planet in planets:
            if sun_x + planet["distance"] > width - 50:
                break

            # 轨道
            draw.ellipse(
                (
                    sun_x - planet["distance"],
                    sun_y - planet["distance"] // 3,
                    sun_x + planet["distance"],
                    sun_y + planet["distance"] // 3,
                ),
                outline=0,
                width=1,
            )

            # 行星
            planet_x = sun_x + planet["distance"]
            planet_y = sun_y
            size = planet["size"]
            draw.ellipse(
                (planet_x - size, planet_y - size, planet_x + size, planet_y + size),
                fill=0,
            )

            # 行星名称
            r.draw_centered_text(draw, planet_x, planet_y + size + 15, planet["name"], r.font_xs)

            # 土星光环
            if planet["name"] == "Saturn":
                draw.ellipse(
                    (planet_x - size - 8, planet_y - 5, planet_x + size + 8, planet_y + 5),
                    outline=0,
                    width=2,
                )

    def _draw_starship(self, draw, width, height):
        """绘制 SpaceX 星舰壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "SpaceX Starship", r.font_l)

        # 星舰主体（简化版）
        ship_x = center_x
        ship_y = center_y + 50

        # 火箭主体（圆柱形）
        draw.rectangle((ship_x - 40, ship_y - 150, ship_x + 40, ship_y + 50), outline=0, width=3)

        # 顶部锥形
        draw.polygon(
            [(ship_x, ship_y - 200), (ship_x - 40, ship_y - 150), (ship_x + 40, ship_y - 150)],
            fill=0,
        )

        # 窗口
        for i in range(3):
            window_y = ship_y - 120 + i * 40
            draw.ellipse(
                (ship_x - 15, window_y - 10, ship_x + 15, window_y + 10), outline=0, width=2
            )

        # 引擎（底部）
        for i in range(-1, 2):
            engine_x = ship_x + i * 25
            draw.rectangle((engine_x - 8, ship_y + 50, engine_x + 8, ship_y + 70), fill=0)

        # 火焰
        for i in range(-1, 2):
            flame_x = ship_x + i * 25
            draw.polygon(
                [
                    (flame_x - 10, ship_y + 70),
                    (flame_x + 10, ship_y + 70),
                    (flame_x, ship_y + 120),
                ],
                fill=0,
            )

        # 地面
        draw.line((50, ship_y + 150, width - 50, ship_y + 150), fill=0, width=3)

        # 文字
        r.draw_centered_text(draw, center_x, height - 40, "To Mars and Beyond", r.font_m)

    def _draw_earth_rise(self, draw, width, height):
        """绘制地出壁纸（从月球看地球升起）"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Earthrise", r.font_l)

        # 月球表面（前景）
        horizon_y = height - 150
        draw.arc((0, horizon_y - 500, width, horizon_y + 500), 0, 180, fill=0, width=5)

        # 陨石坑
        craters = [(150, horizon_y - 80, 30), (400, horizon_y - 60, 25), (600, horizon_y - 90, 35)]
        for cx, cy, size in craters:
            draw.ellipse((cx - size, cy - size, cx + size, cy + size), fill=0)

        # 地球（背景）
        earth_x = width - 200
        earth_y = 200
        earth_size = 80

        # 地球主体
        draw.ellipse(
            (
                earth_x - earth_size,
                earth_y - earth_size,
                earth_x + earth_size,
                earth_y + earth_size,
            ),
            outline=0,
            width=3,
        )

        # 大陆
        r.draw_icon_earth(draw, earth_x, earth_y, size=earth_size * 2)

        # 星空
        import random

        random.seed(42)  # 固定种子保证每次相同
        for _ in range(50):
            star_x = random.randint(50, width - 50)
            star_y = random.randint(50, horizon_y - 100)
            draw.point((star_x, star_y), fill=0)

    def _draw_saturn_rings(self, draw, width, height):
        """绘制土星特写壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Saturn - Lord of the Rings", r.font_l)

        # 土星主体（大）
        saturn_size = 150
        draw.ellipse(
            (
                center_x - saturn_size,
                center_y - saturn_size,
                center_x + saturn_size,
                center_y + saturn_size,
            ),
            outline=0,
            width=4,
        )

        # 光环（多层）
        for i in range(5):
            ring_size = saturn_size + 30 + i * 20
            ring_height = 30 + i * 10
            draw.ellipse(
                (
                    center_x - ring_size,
                    center_y - ring_height,
                    center_x + ring_size,
                    center_y + ring_height,
                ),
                outline=0,
                width=2,
            )

        # 擦除被行星遮挡的部分
        draw.ellipse(
            (
                center_x - saturn_size + 5,
                center_y - saturn_size + 5,
                center_x + saturn_size - 5,
                center_y + saturn_size - 5,
            ),
            fill=255,
        )

        # 重新绘制行星轮廓
        draw.ellipse(
            (
                center_x - saturn_size,
                center_y - saturn_size,
                center_x + saturn_size,
                center_y + saturn_size,
            ),
            outline=0,
            width=4,
        )

    def _draw_galaxy(self, draw, width, height):
        """绘制星系壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Milky Way Galaxy", r.font_l)

        # 星系核心
        draw.ellipse((center_x - 50, center_y - 50, center_x + 50, center_y + 50), fill=0)

        # 旋臂
        import math

        for arm in range(4):
            angle_offset = arm * math.pi / 2
            for i in range(100):
                angle = angle_offset + i * 0.1
                distance = 60 + i * 3
                x = center_x + int(distance * math.cos(angle))
                y = center_y + int(distance * math.sin(angle))
                if 0 < x < width and 0 < y < height:
                    size = max(1, 5 - i // 20)
                    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)

    def _draw_moon_landing(self, draw, width, height):
        """绘制登月壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "One Small Step", r.font_l)

        # 月球表面
        horizon_y = height - 100
        draw.line((0, horizon_y, width, horizon_y), fill=0, width=3)

        # 登月舱
        lander_x = 200
        lander_y = horizon_y - 80
        draw.polygon(
            [
                (lander_x, lander_y - 40),
                (lander_x - 30, lander_y),
                (lander_x + 30, lander_y),
            ],
            fill=0,
        )
        # 支架
        draw.line((lander_x - 25, lander_y, lander_x - 40, horizon_y), fill=0, width=2)
        draw.line((lander_x + 25, lander_y, lander_x + 40, horizon_y), fill=0, width=2)

        # 宇航员
        astro_x = 400
        # 头盔
        draw.ellipse(
            (astro_x - 15, horizon_y - 70, astro_x + 15, horizon_y - 40), outline=0, width=2
        )
        # 身体
        draw.rectangle((astro_x - 20, horizon_y - 40, astro_x + 20, horizon_y), outline=0, width=2)
        # 腿
        draw.line((astro_x - 10, horizon_y, astro_x - 15, horizon_y + 20), fill=0, width=2)
        draw.line((astro_x + 10, horizon_y, astro_x + 15, horizon_y + 20), fill=0, width=2)

        # 脚印
        for i in range(5):
            foot_x = astro_x + 50 + i * 40
            draw.ellipse((foot_x - 10, horizon_y + 5, foot_x + 10, horizon_y + 15), fill=0)

        # 地球（远景）
        earth_x = width - 150
        earth_y = 150
        r.draw_icon_earth(draw, earth_x, earth_y, size=60)

    def _draw_mars_landscape(self, draw, width, height):
        """绘制火星景观壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Mars - The Red Planet", r.font_l)

        # 地平线
        horizon_y = height - 150

        # 山脉
        mountains = [
            (100, horizon_y - 80),
            (250, horizon_y - 120),
            (400, horizon_y - 60),
            (550, horizon_y - 100),
            (700, horizon_y - 70),
        ]
        for i, (mx, my) in enumerate(mountains):
            draw.polygon([(mx - 80, horizon_y), (mx, my), (mx + 80, horizon_y)], fill=0)

        # 火星车
        rover_x = 150
        rover_y = horizon_y - 30
        # 车身
        draw.rectangle((rover_x - 30, rover_y - 20, rover_x + 30, rover_y), outline=0, width=2)
        # 轮子
        for wx in [rover_x - 20, rover_x + 20]:
            draw.ellipse((wx - 8, rover_y, wx + 8, rover_y + 16), fill=0)
        # 天线
        draw.line((rover_x, rover_y - 20, rover_x, rover_y - 40), fill=0, width=2)
        draw.ellipse((rover_x - 5, rover_y - 45, rover_x + 5, rover_y - 35), fill=0)

    def _draw_nebula(self, draw, width, height):
        """绘制星云壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Nebula - Stellar Nursery", r.font_l)

        # 星云云团（用多个椭圆模拟）
        import random

        random.seed(123)
        for _ in range(20):
            x = random.randint(100, width - 100)
            y = random.randint(100, height - 100)
            w = random.randint(40, 100)
            h = random.randint(30, 80)
            draw.ellipse((x - w, y - h, x + w, y + h), outline=0, width=1)

        # 新生恒星（亮点）
        for _ in range(30):
            sx = random.randint(100, width - 100)
            sy = random.randint(100, height - 100)
            size = random.randint(2, 5)
            draw.ellipse((sx - size, sy - size, sx + size, sy + size), fill=0)

    # --- Nature Theme Wallpapers ---

    def _draw_snow_mountain(self, draw, width, height):
        """绘制雪山壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Snowy Mountains", r.font_l)

        # 天空和云
        for i in range(3):
            cloud_x = 150 + i * 250
            cloud_y = 100 + i * 20
            draw.ellipse(
                (cloud_x - 40, cloud_y - 15, cloud_x + 40, cloud_y + 15), outline=0, width=2
            )

        # 远山
        far_mountains = [(200, 200), (400, 180), (600, 210)]
        for mx, my in far_mountains:
            draw.polygon(
                [(mx - 100, height - 100), (mx, my), (mx + 100, height - 100)], outline=0, width=2
            )

        # 主峰（雪山）
        peak_x = center_x
        peak_y = 120
        draw.polygon(
            [(peak_x - 150, height - 100), (peak_x, peak_y), (peak_x + 150, height - 100)],
            fill=0,
        )
        # 雪线（白色三角形）
        draw.polygon(
            [(peak_x - 80, peak_y + 100), (peak_x, peak_y), (peak_x + 80, peak_y + 100)],
            fill=255,
            outline=0,
        )

        # 前景树林
        for i in range(8):
            tree_x = 100 + i * 90
            tree_y = height - 100
            # 树干
            draw.line((tree_x, tree_y, tree_x, tree_y - 40), fill=0, width=3)
            # 树冠
            draw.polygon(
                [(tree_x - 15, tree_y - 40), (tree_x, tree_y - 70), (tree_x + 15, tree_y - 40)],
                fill=0,
            )

    def _draw_cherry_blossom(self, draw, width, height):
        """绘制樱花壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Cherry Blossom - 桜", r.font_l)

        # 樱花树干
        tree_x = 150
        draw.line((tree_x, height, tree_x, 200), fill=0, width=8)
        draw.line((tree_x, 300, tree_x + 100, 200), fill=0, width=5)
        draw.line((tree_x, 250, tree_x - 80, 180), fill=0, width=5)

        # 樱花（小圆圈）
        import random

        random.seed(456)
        for _ in range(60):
            bx = random.randint(50, 300)
            by = random.randint(100, 350)
            size = random.randint(3, 8)
            # 花瓣（5瓣）
            for i in range(5):
                import math

                angle = i * 72
                px = bx + int(size * math.cos(math.radians(angle)))
                py = by + int(size * math.sin(math.radians(angle)))
                draw.ellipse((px - 2, py - 2, px + 2, py + 2), fill=0)

        # 远景山
        draw.arc((width - 300, 200, width - 100, 400), 0, 180, fill=0, width=3)

        # 诗句
        r.draw_centered_text(draw, width - 200, height - 80, "花见 Hanami", r.font_m)

    def _draw_sunset_beach(self, draw, width, height):
        """绘制海边日落壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Sunset Beach", r.font_l)

        # 太阳
        sun_x = width - 200
        sun_y = 180
        for i in range(3):
            draw.ellipse(
                (
                    sun_x - 40 - i * 10,
                    sun_y - 40 - i * 10,
                    sun_x + 40 + i * 10,
                    sun_y + 40 + i * 10,
                ),
                outline=0,
                width=2,
            )

        # 海平线
        horizon_y = height - 200
        draw.line((0, horizon_y, width, horizon_y), fill=0, width=3)

        # 波浪
        for i in range(5):
            wave_y = horizon_y + 30 + i * 30
            for x in range(0, width, 60):
                draw.arc((x, wave_y - 15, x + 60, wave_y + 15), 0, 180, fill=0, width=2)

        # 椰子树
        palm_x = 150
        palm_y = horizon_y - 20
        draw.line((palm_x, palm_y, palm_x + 20, palm_y - 100), fill=0, width=4)
        # 树叶
        for i in range(6):
            import math

            angle = i * 60
            leaf_len = 50
            end_x = palm_x + 20 + int(leaf_len * math.cos(math.radians(angle)))
            end_y = palm_y - 100 + int(leaf_len * math.sin(math.radians(angle)))
            draw.line((palm_x + 20, palm_y - 100, end_x, end_y), fill=0, width=3)

    def _draw_forest_path(self, draw, width, height):
        """绘制森林小径壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Forest Path", r.font_l)

        # 小径（透视）
        path_top_y = 200
        path_bottom_y = height - 50
        draw.polygon(
            [
                (center_x - 150, path_bottom_y),
                (center_x - 50, path_top_y),
                (center_x + 50, path_top_y),
                (center_x + 150, path_bottom_y),
            ],
            outline=0,
            width=3,
        )

        # 两侧树木
        for side in [-1, 1]:
            for i in range(5):
                tree_x = center_x + side * (200 + i * 30)
                tree_y = path_top_y + i * 80
                tree_height = 150 - i * 20
                # 树干
                draw.line((tree_x, tree_y + 50, tree_x, tree_y + 50 - tree_height), fill=0, width=5)
                # 树冠
                draw.ellipse(
                    (tree_x - 30, tree_y - 30, tree_x + 30, tree_y + 30),
                    outline=0,
                    width=2,
                )

        # 阳光（射线）
        for i in range(5):
            ray_x = center_x - 100 + i * 50
            draw.line((ray_x, 100, ray_x + 20, path_top_y), fill=0, width=1)

    def _draw_northern_lights(self, draw, width, height):
        """绘制极光壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Aurora Borealis", r.font_l)

        # 极光（波浪形）
        import math

        for wave in range(3):
            y_offset = 150 + wave * 40
            points = []
            for x in range(0, width, 20):
                y = y_offset + int(30 * math.sin(x / 50 + wave))
                points.append((x, y))
            for i in range(len(points) - 1):
                draw.line(
                    (points[i][0], points[i][1], points[i + 1][0], points[i + 1][1]),
                    fill=0,
                    width=3,
                )

        # 地平线（雪地）
        horizon_y = height - 150
        draw.line((0, horizon_y, width, horizon_y), fill=0, width=3)

        # 雪山轮廓
        for i in range(4):
            mx = 150 + i * 180
            my = horizon_y - 80 - i * 10
            draw.polygon([(mx - 60, horizon_y), (mx, my), (mx + 60, horizon_y)], outline=0, width=2)

        # 星星
        import random

        random.seed(789)
        for _ in range(40):
            sx = random.randint(50, width - 50)
            sy = random.randint(50, horizon_y - 50)
            draw.point((sx, sy), fill=0)

    # --- Warm Theme Wallpapers ---

    def _draw_family_home(self, draw, width, height):
        """绘制温馨家庭壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Home Sweet Home", r.font_l)

        # 房子
        house_x = center_x
        house_y = center_y + 50
        # 墙
        draw.rectangle(
            (house_x - 100, house_y - 80, house_x + 100, house_y + 50), outline=0, width=3
        )
        # 屋顶
        draw.polygon(
            [
                (house_x - 120, house_y - 80),
                (house_x, house_y - 150),
                (house_x + 120, house_y - 80),
            ],
            fill=0,
        )
        # 门
        draw.rectangle((house_x - 20, house_y, house_x + 20, house_y + 50), outline=0, width=2)
        # 窗户
        draw.rectangle((house_x - 70, house_y - 50, house_x - 30, house_y - 10), outline=0, width=2)
        draw.rectangle((house_x + 30, house_y - 50, house_x + 70, house_y - 10), outline=0, width=2)
        # 窗户十字
        draw.line((house_x - 50, house_y - 50, house_x - 50, house_y - 10), fill=0, width=1)
        draw.line((house_x - 70, house_y - 30, house_x - 30, house_y - 30), fill=0, width=1)

        # 烟囱
        draw.rectangle((house_x + 50, house_y - 150, house_x + 70, house_y - 120), fill=0)
        # 烟
        for i in range(3):
            smoke_y = house_y - 150 - i * 15
            draw.ellipse((house_x + 55, smoke_y - 10, house_x + 65, smoke_y), outline=0, width=1)

        # 家人（简笔画）
        # 爸爸
        dad_x = house_x - 150
        draw.ellipse((dad_x - 10, house_y - 30, dad_x + 10, house_y - 10), outline=0, width=2)
        draw.line((dad_x, house_y - 10, dad_x, house_y + 30), fill=0, width=2)
        # 妈妈
        mom_x = house_x - 120
        draw.ellipse((mom_x - 10, house_y - 25, mom_x + 10, house_y - 5), outline=0, width=2)
        draw.line((mom_x, house_y - 5, mom_x, house_y + 30), fill=0, width=2)
        # 孩子
        kid_x = house_x - 135
        draw.ellipse((kid_x - 8, house_y + 5, kid_x + 8, house_y + 20), outline=0, width=2)
        draw.line((kid_x, house_y + 20, kid_x, house_y + 30), fill=0, width=2)

        # 爱心
        r.draw_icon_heart(draw, house_x, house_y - 200, size=40)

    def _draw_couple_love(self, draw, width, height):
        """绘制恋人壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Love Forever", r.font_l)

        # 两个人（简笔画）
        # 左边（女）
        girl_x = center_x - 60
        draw.ellipse((girl_x - 15, center_y - 40, girl_x + 15, center_y - 10), outline=0, width=2)
        draw.line((girl_x, center_y - 10, girl_x, center_y + 40), fill=0, width=2)
        # 裙子
        draw.polygon(
            [(girl_x - 20, center_y + 10), (girl_x, center_y + 40), (girl_x + 20, center_y + 10)],
            outline=0,
            width=2,
        )

        # 右边（男）
        boy_x = center_x + 60
        draw.ellipse((boy_x - 15, center_y - 45, boy_x + 15, center_y - 15), outline=0, width=2)
        draw.line((boy_x, center_y - 15, boy_x, center_y + 40), fill=0, width=2)
        # 裤子
        draw.line((boy_x - 10, center_y + 10, boy_x - 10, center_y + 40), fill=0, width=2)
        draw.line((boy_x + 10, center_y + 10, boy_x + 10, center_y + 40), fill=0, width=2)

        # 牵手
        draw.line((girl_x + 15, center_y, boy_x - 15, center_y), fill=0, width=3)

        # 爱心（多个）
        hearts = [
            (center_x, center_y - 100, 50),
            (center_x - 80, center_y - 120, 30),
            (center_x + 80, center_y - 110, 35),
        ]
        for hx, hy, hsize in hearts:
            r.draw_icon_heart(draw, hx, hy, size=hsize)

        # 文字
        r.draw_centered_text(draw, center_x, height - 60, "Together Forever", r.font_m)

    def _draw_coffee_time(self, draw, width, height):
        """绘制咖啡时光壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Coffee Time", r.font_l)

        # 咖啡杯
        cup_x = center_x - 80
        cup_y = center_y
        # 杯身
        draw.polygon(
            [
                (cup_x - 40, cup_y - 30),
                (cup_x - 50, cup_y + 40),
                (cup_x + 50, cup_y + 40),
                (cup_x + 40, cup_y - 30),
            ],
            outline=0,
            width=3,
        )
        # 杯口
        draw.ellipse((cup_x - 40, cup_y - 35, cup_x + 40, cup_y - 25), outline=0, width=2)
        # 把手
        draw.arc((cup_x + 40, cup_y - 10, cup_x + 70, cup_y + 30), 270, 90, fill=0, width=3)
        # 热气
        for i in range(3):
            steam_x = cup_x - 20 + i * 20
            draw.arc((steam_x - 10, cup_y - 60, steam_x + 10, cup_y - 40), 0, 180, fill=0, width=2)

        # 书
        book_x = center_x + 80
        book_y = center_y + 20
        draw.rectangle((book_x - 50, book_y - 30, book_x + 50, book_y + 30), outline=0, width=3)
        # 书页
        for i in range(3):
            draw.line(
                (book_x - 40 + i * 30, book_y - 20, book_x - 40 + i * 30, book_y + 20),
                fill=0,
                width=1,
            )

        # 桌子
        table_y = center_y + 60
        draw.line((100, table_y, width - 100, table_y), fill=0, width=4)

        # 文字
        r.draw_centered_text(draw, center_x, height - 60, "Relax & Enjoy", r.font_m)

    def _draw_reading_room(self, draw, width, height):
        """绘制书房壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Reading Room", r.font_l)

        # 书架
        shelf_x = 150
        shelf_y = 150
        for row in range(3):
            y = shelf_y + row * 80
            draw.line((shelf_x, y, shelf_x + 200, y), fill=0, width=3)
            # 书
            for i in range(8):
                book_x = shelf_x + 10 + i * 24
                book_height = 50 + (i % 3) * 10
                draw.rectangle((book_x, y - book_height, book_x + 20, y), outline=0, width=2)

        # 椅子
        chair_x = center_x + 150
        chair_y = height - 150
        # 座位
        draw.rectangle((chair_x - 40, chair_y, chair_x + 40, chair_y + 20), fill=0)
        # 靠背
        draw.rectangle((chair_x - 40, chair_y - 60, chair_x - 30, chair_y), outline=0, width=2)
        # 腿
        draw.line((chair_x - 35, chair_y + 20, chair_x - 35, chair_y + 50), fill=0, width=3)
        draw.line((chair_x + 35, chair_y + 20, chair_x + 35, chair_y + 50), fill=0, width=3)

        # 台灯
        lamp_x = center_x + 200
        lamp_y = height - 200
        # 灯罩
        draw.polygon(
            [
                (lamp_x - 30, lamp_y),
                (lamp_x - 20, lamp_y - 30),
                (lamp_x + 20, lamp_y - 30),
                (lamp_x + 30, lamp_y),
            ],
            outline=0,
            width=2,
        )
        # 灯杆
        draw.line((lamp_x, lamp_y, lamp_x, lamp_y + 50), fill=0, width=2)
        # 底座
        draw.ellipse((lamp_x - 20, lamp_y + 50, lamp_x + 20, lamp_y + 60), fill=0)

    def _draw_rainy_window(self, draw, width, height):
        """绘制雨窗壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Rainy Day", r.font_l)

        # 窗框
        draw.rectangle((150, 120, width - 150, height - 120), outline=0, width=4)
        # 十字窗格
        draw.line((center_x, 120, center_x, height - 120), fill=0, width=3)
        draw.line((150, center_y, width - 150, center_y), fill=0, width=3)

        # 雨滴
        import random

        random.seed(999)
        for _ in range(50):
            rx = random.randint(160, width - 160)
            ry = random.randint(130, height - 130)
            drop_len = random.randint(10, 25)
            draw.line((rx, ry, rx + 2, ry + drop_len), fill=0, width=1)

        # 窗台上的植物
        plant_x = center_x - 100
        plant_y = height - 130
        # 花盆
        draw.polygon(
            [
                (plant_x - 30, plant_y),
                (plant_x - 20, plant_y + 30),
                (plant_x + 20, plant_y + 30),
                (plant_x + 30, plant_y),
            ],
            outline=0,
            width=2,
        )
        # 叶子
        for i in range(5):
            leaf_x = plant_x - 20 + i * 10
            draw.ellipse(
                (leaf_x - 5, plant_y - 20 - i * 5, leaf_x + 5, plant_y - i * 5), outline=0, width=2
            )

        # 热茶
        tea_x = center_x + 100
        tea_y = height - 140
        # 杯子
        draw.polygon(
            [
                (tea_x - 20, tea_y),
                (tea_x - 25, tea_y + 30),
                (tea_x + 25, tea_y + 30),
                (tea_x + 20, tea_y),
            ],
            outline=0,
            width=2,
        )
        # 热气
        for i in range(2):
            steam_x = tea_x - 10 + i * 20
            draw.arc((steam_x - 8, tea_y - 20, steam_x + 8, tea_y - 5), 0, 180, fill=0, width=2)

    # --- Animal & Plant Theme Wallpapers ---

    def _draw_cat_nap(self, draw, width, height):
        """绘制猫咪午睡壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Cat Nap", r.font_l)

        # 猫（简笔画）
        cat_x = center_x
        cat_y = center_y

        # 身体（椭圆）
        draw.ellipse((cat_x - 60, cat_y - 30, cat_x + 60, cat_y + 30), outline=0, width=3)

        # 头
        draw.ellipse((cat_x + 40, cat_y - 50, cat_x + 80, cat_y - 10), outline=0, width=3)

        # 耳朵
        draw.polygon(
            [(cat_x + 45, cat_y - 50), (cat_x + 50, cat_y - 70), (cat_x + 60, cat_y - 50)], fill=0
        )
        draw.polygon(
            [(cat_x + 70, cat_y - 50), (cat_x + 75, cat_y - 70), (cat_x + 85, cat_y - 50)], fill=0
        )

        # 眼睛（闭着）
        draw.line((cat_x + 50, cat_y - 35, cat_x + 55, cat_y - 35), fill=0, width=2)
        draw.line((cat_x + 65, cat_y - 35, cat_x + 70, cat_y - 35), fill=0, width=2)

        # 鼻子
        draw.ellipse((cat_x + 58, cat_y - 28, cat_x + 62, cat_y - 24), fill=0)

        # 胡须
        for i in range(-1, 2):
            y_offset = i * 5
            draw.line(
                (cat_x + 40, cat_y - 25 + y_offset, cat_x + 20, cat_y - 25 + y_offset),
                fill=0,
                width=1,
            )
            draw.line(
                (cat_x + 80, cat_y - 25 + y_offset, cat_x + 100, cat_y - 25 + y_offset),
                fill=0,
                width=1,
            )

        # 尾巴
        draw.arc((cat_x - 60, cat_y, cat_x - 20, cat_y + 60), 180, 270, fill=0, width=3)

        # 垫子
        draw.ellipse((cat_x - 80, cat_y + 25, cat_x + 80, cat_y + 50), outline=0, width=2)

        # Zzz
        for i in range(3):
            z_x = cat_x + 100 + i * 20
            z_y = cat_y - 80 - i * 15
            r.draw_centered_text(draw, z_x, z_y, "Z", r.font_m)

    def _draw_dog_play(self, draw, width, height):
        """绘制小狗玩耍壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Playful Dog", r.font_l)

        # 小狗
        dog_x = center_x - 80
        dog_y = center_y

        # 身体
        draw.ellipse((dog_x - 40, dog_y - 25, dog_x + 40, dog_y + 25), outline=0, width=3)

        # 头
        draw.ellipse((dog_x + 30, dog_y - 40, dog_x + 70, dog_y), outline=0, width=3)

        # 耳朵（下垂）
        draw.ellipse((dog_x + 25, dog_y - 35, dog_x + 35, dog_y - 10), fill=0)
        draw.ellipse((dog_x + 65, dog_y - 35, dog_x + 75, dog_y - 10), fill=0)

        # 眼睛
        draw.ellipse((dog_x + 40, dog_y - 30, dog_x + 45, dog_y - 25), fill=0)
        draw.ellipse((dog_x + 55, dog_y - 30, dog_x + 60, dog_y - 25), fill=0)

        # 鼻子
        draw.ellipse((dog_x + 45, dog_y - 18, dog_x + 55, dog_y - 13), fill=0)

        # 嘴巴（微笑）
        draw.arc((dog_x + 35, dog_y - 15, dog_x + 65, dog_y - 5), 0, 180, fill=0, width=2)

        # 腿
        for lx in [dog_x - 25, dog_x - 5, dog_x + 15]:
            draw.line((lx, dog_y + 25, lx, dog_y + 50), fill=0, width=3)

        # 尾巴（摇摆）
        draw.arc((dog_x - 60, dog_y - 30, dog_x - 30, dog_y + 10), 90, 270, fill=0, width=3)

        # 球
        ball_x = center_x + 100
        ball_y = center_y - 20
        draw.ellipse((ball_x - 20, ball_y - 20, ball_x + 20, ball_y + 20), outline=0, width=3)
        # 球的纹路
        draw.line((ball_x - 20, ball_y, ball_x + 20, ball_y), fill=0, width=1)
        draw.line((ball_x, ball_y - 20, ball_x, ball_y + 20), fill=0, width=1)

        # 地面
        draw.line((100, center_y + 60, width - 100, center_y + 60), fill=0, width=3)

    def _draw_bird_tree(self, draw, width, height):
        """绘制小鸟与树壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Birds in Tree", r.font_l)

        # 树干
        tree_x = center_x - 100
        draw.line((tree_x, height - 50, tree_x, 200), fill=0, width=10)

        # 树枝
        branches = [
            (tree_x, 250, tree_x + 100, 220),
            (tree_x, 300, tree_x + 120, 280),
            (tree_x, 350, tree_x + 90, 340),
            (tree_x, 280, tree_x - 80, 260),
        ]
        for x1, y1, x2, y2 in branches:
            draw.line((x1, y1, x2, y2), fill=0, width=5)

        # 树叶（简化）
        for bx, by, _, _ in branches:
            for i in range(3):
                leaf_x = bx + (i - 1) * 30
                draw.ellipse((leaf_x - 15, by - 30, leaf_x + 15, by), outline=0, width=2)

        # 小鸟们
        birds = [
            (tree_x + 80, 210),
            (tree_x + 100, 270),
            (tree_x + 70, 330),
            (center_x + 50, 180),
        ]

        for bird_x, bird_y in birds:
            # 身体
            draw.ellipse((bird_x - 10, bird_y - 8, bird_x + 10, bird_y + 8), fill=0)
            # 头
            draw.ellipse((bird_x + 6, bird_y - 12, bird_x + 16, bird_y - 2), outline=0, width=2)
            # 眼睛
            draw.point((bird_x + 10, bird_y - 8), fill=0)
            # 翅膀
            draw.arc((bird_x - 10, bird_y - 5, bird_x + 5, bird_y + 10), 180, 270, fill=0, width=2)
            # 尾巴
            draw.line((bird_x - 10, bird_y, bird_x - 18, bird_y + 5), fill=0, width=2)

        # 音符（鸟鸣）
        notes_x = center_x + 80
        r.draw_centered_text(draw, notes_x, 150, "♪", r.font_l)
        r.draw_centered_text(draw, notes_x + 30, 170, "♫", r.font_l)

    def _draw_butterfly_garden(self, draw, width, height):
        """绘制蝴蝶花园壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Butterfly Garden", r.font_l)

        # 花朵
        flowers = [
            (200, height - 150, 30),
            (350, height - 130, 35),
            (500, height - 160, 28),
            (650, height - 140, 32),
        ]

        for fx, fy, fsize in flowers:
            # 花茎
            draw.line((fx, fy, fx, fy + 100), fill=0, width=3)
            # 花瓣（5瓣）
            for i in range(5):
                import math

                angle = i * 72
                px = fx + int(fsize * math.cos(math.radians(angle)))
                py = fy + int(fsize * math.sin(math.radians(angle)))
                draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=0)
            # 花心
            draw.ellipse((fx - 10, fy - 10, fx + 10, fy + 10), outline=0, width=2)

        # 蝴蝶
        butterflies = [
            (300, 200),
            (500, 250),
            (400, 180),
        ]

        for bx, by in butterflies:
            # 身体
            draw.ellipse((bx - 3, by - 15, bx + 3, by + 15), fill=0)
            # 触角
            draw.line((bx - 2, by - 15, bx - 8, by - 25), fill=0, width=1)
            draw.line((bx + 2, by - 15, bx + 8, by - 25), fill=0, width=1)
            draw.ellipse((bx - 10, by - 27, bx - 6, by - 23), fill=0)
            draw.ellipse((bx + 6, by - 27, bx + 10, by - 23), fill=0)

            # 翅膀（左上）
            draw.ellipse((bx - 25, by - 20, bx - 5, by), outline=0, width=2)
            # 翅膀（左下）
            draw.ellipse((bx - 20, by, bx - 5, by + 15), outline=0, width=2)
            # 翅膀（右上）
            draw.ellipse((bx + 5, by - 20, bx + 25, by), outline=0, width=2)
            # 翅膀（右下）
            draw.ellipse((bx + 5, by, bx + 20, by + 15), outline=0, width=2)

        # 草地
        draw.line((0, height - 100, width, height - 100), fill=0, width=3)

    def _draw_whale_ocean(self, draw, width, height):
        """绘制鲸鱼海洋壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Whale in Ocean", r.font_l)

        # 海平面
        sea_y = center_y + 50
        draw.line((0, sea_y, width, sea_y), fill=0, width=3)

        # 波浪
        for i in range(3):
            wave_y = sea_y + 30 + i * 25
            for x in range(0, width, 80):
                draw.arc((x, wave_y - 12, x + 80, wave_y + 12), 0, 180, fill=0, width=2)

        # 鲸鱼（在水中）
        whale_x = center_x
        whale_y = center_y + 100

        # 身体
        draw.ellipse((whale_x - 80, whale_y - 30, whale_x + 80, whale_y + 30), outline=0, width=3)

        # 头部
        draw.arc(
            (whale_x + 60, whale_y - 35, whale_x + 100, whale_y + 35), 270, 90, fill=0, width=3
        )

        # 眼睛
        draw.ellipse((whale_x + 50, whale_y - 15, whale_x + 55, whale_y - 10), fill=0)

        # 嘴巴
        draw.arc((whale_x + 70, whale_y - 5, whale_x + 90, whale_y + 15), 0, 90, fill=0, width=2)

        # 尾巴
        draw.polygon(
            [(whale_x - 80, whale_y), (whale_x - 110, whale_y - 25), (whale_x - 110, whale_y + 25)],
            outline=0,
            width=2,
        )

        # 鳍
        draw.arc((whale_x - 20, whale_y + 25, whale_x + 20, whale_y + 60), 0, 180, fill=0, width=3)

        # 水柱
        for i in range(3):
            spray_x = whale_x + 30 + i * 15
            spray_y = whale_y - 40 - i * 20
            draw.line((spray_x, whale_y - 30, spray_x, spray_y), fill=0, width=2)
            draw.ellipse((spray_x - 5, spray_y - 10, spray_x + 5, spray_y), outline=0, width=1)

    def _draw_panda_bamboo(self, draw, width, height):
        """绘制熊猫竹林壁纸"""
        r = self.renderer
        center_x = width // 2
        center_y = height // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Panda & Bamboo", r.font_l)

        # 竹子
        for i in range(5):
            bamboo_x = 150 + i * 120
            bamboo_h = 300 + (i % 2) * 50
            # 竹竿
            draw.line((bamboo_x, height - 100, bamboo_x, height - 100 - bamboo_h), fill=0, width=5)
            # 竹节
            for j in range(4):
                node_y = height - 100 - j * 80
                draw.line((bamboo_x - 10, node_y, bamboo_x + 10, node_y), fill=0, width=3)
            # 竹叶
            for j in range(3):
                leaf_y = height - 150 - j * 80
                draw.line((bamboo_x, leaf_y, bamboo_x - 25, leaf_y - 15), fill=0, width=2)
                draw.line((bamboo_x, leaf_y, bamboo_x + 25, leaf_y - 15), fill=0, width=2)

        # 熊猫
        panda_x = center_x
        panda_y = center_y + 50

        # 身体
        draw.ellipse((panda_x - 50, panda_y - 40, panda_x + 50, panda_y + 40), outline=0, width=3)
        draw.ellipse((panda_x - 45, panda_y - 35, panda_x + 45, panda_y + 35), fill=255)

        # 头
        draw.ellipse((panda_x - 40, panda_y - 80, panda_x + 40, panda_y - 20), outline=0, width=3)
        draw.ellipse((panda_x - 35, panda_y - 75, panda_x + 35, panda_y - 25), fill=255)

        # 耳朵（黑色）
        draw.ellipse((panda_x - 40, panda_y - 85, panda_x - 20, panda_y - 65), fill=0)
        draw.ellipse((panda_x + 20, panda_y - 85, panda_x + 40, panda_y - 65), fill=0)

        # 眼睛（黑眼圈）
        draw.ellipse((panda_x - 25, panda_y - 60, panda_x - 10, panda_y - 45), fill=0)
        draw.ellipse((panda_x + 10, panda_y - 60, panda_x + 25, panda_y - 45), fill=0)
        # 眼珠（白色）
        draw.ellipse((panda_x - 20, panda_y - 55, panda_x - 15, panda_y - 50), fill=255)
        draw.ellipse((panda_x + 15, panda_y - 55, panda_x + 20, panda_y - 50), fill=255)

        # 鼻子
        draw.ellipse((panda_x - 8, panda_y - 45, panda_x + 8, panda_y - 37), fill=0)

        # 嘴巴
        draw.arc((panda_x - 15, panda_y - 40, panda_x + 15, panda_y - 25), 0, 180, fill=0, width=2)

        # 四肢（黑色）
        # 前腿
        draw.ellipse((panda_x - 45, panda_y + 10, panda_x - 25, panda_y + 50), fill=0)
        draw.ellipse((panda_x + 25, panda_y + 10, panda_x + 45, panda_y + 50), fill=0)

    def _draw_flower_meadow(self, draw, width, height):
        """绘制花草地壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Flower Meadow", r.font_l)

        # 地平线
        horizon_y = height - 200

        # 远山
        draw.arc((100, horizon_y - 100, 300, horizon_y + 100), 0, 180, fill=0, width=2)
        draw.arc((400, horizon_y - 80, 600, horizon_y + 120), 0, 180, fill=0, width=2)

        # 草地
        import random

        random.seed(111)
        for _ in range(30):
            grass_x = random.randint(50, width - 50)
            grass_y = random.randint(horizon_y, height - 50)
            grass_h = random.randint(15, 30)
            draw.line((grass_x, grass_y, grass_x + 3, grass_y - grass_h), fill=0, width=2)

        # 各种花朵
        flowers_data = [
            (150, height - 150, "daisy"),
            (250, height - 130, "tulip"),
            (380, height - 160, "daisy"),
            (520, height - 140, "sunflower"),
            (650, height - 155, "tulip"),
        ]

        for fx, fy, flower_type in flowers_data:
            # 花茎
            draw.line((fx, fy, fx, fy + 80), fill=0, width=3)

            match flower_type:
                case "daisy":
                    # 雏菊 - 花瓣
                    for i in range(8):
                        import math

                        angle = i * 45
                        px = fx + int(20 * math.cos(math.radians(angle)))
                        py = fy + int(20 * math.sin(math.radians(angle)))
                        draw.ellipse((px - 5, py - 8, px + 5, py + 8), fill=0)
                    # 花心
                    draw.ellipse((fx - 8, fy - 8, fx + 8, fy + 8), outline=0, width=2)

                case "tulip":
                    # 郁金香
                    draw.ellipse((fx - 15, fy - 25, fx + 15, fy + 5), outline=0, width=2)
                    draw.arc((fx - 15, fy - 25, fx + 15, fy + 5), 0, 180, fill=0, width=2)

                case "sunflower":
                    # 向日葵
                    for i in range(12):
                        import math

                        angle = i * 30
                        px = fx + int(25 * math.cos(math.radians(angle)))
                        py = fy + int(25 * math.sin(math.radians(angle)))
                        draw.ellipse((px - 6, py - 10, px + 6, py + 10), fill=0)
                    # 花心（大）
                    draw.ellipse((fx - 12, fy - 12, fx + 12, fy + 12), fill=0)

        # 蜜蜂
        bee_x = 400
        bee_y = 200
        # 身体
        draw.ellipse((bee_x - 10, bee_y - 6, bee_x + 10, bee_y + 6), fill=0)
        # 条纹（白色）
        draw.line((bee_x - 3, bee_y - 6, bee_x - 3, bee_y + 6), fill=255, width=3)
        draw.line((bee_x + 3, bee_y - 6, bee_x + 3, bee_y + 6), fill=255, width=3)
        # 翅膀
        draw.ellipse((bee_x - 8, bee_y - 12, bee_x + 2, bee_y - 2), outline=0, width=1)
        draw.ellipse((bee_x - 2, bee_y - 12, bee_x + 8, bee_y - 2), outline=0, width=1)

    def _draw_cactus_desert(self, draw, width, height):
        """绘制仙人掌沙漠壁纸"""
        r = self.renderer
        center_x = width // 2

        # 标题
        r.draw_centered_text(draw, center_x, 30, "Cactus Desert", r.font_l)

        # 太阳
        sun_x = width - 150
        sun_y = 120
        draw.ellipse((sun_x - 40, sun_y - 40, sun_x + 40, sun_y + 40), fill=0)

        # 地平线
        horizon_y = height - 150
        draw.line((0, horizon_y, width, horizon_y), fill=0, width=3)

        # 沙丘
        dunes = [(200, horizon_y), (500, horizon_y), (700, horizon_y)]
        for dx, dy in dunes:
            draw.arc((dx - 100, dy - 50, dx + 100, dy + 50), 0, 180, fill=0, width=2)

        # 仙人掌们
        # 大仙人掌（柱状）
        cactus1_x = 250
        cactus1_y = horizon_y - 150
        # 主干
        draw.rectangle((cactus1_x - 20, cactus1_y, cactus1_x + 20, horizon_y), outline=0, width=3)
        # 左臂
        draw.line((cactus1_x - 20, cactus1_y + 50, cactus1_x - 50, cactus1_y + 50), fill=0, width=3)
        draw.line((cactus1_x - 50, cactus1_y + 50, cactus1_x - 50, cactus1_y + 20), fill=0, width=3)
        draw.arc(
            (cactus1_x - 70, cactus1_y + 20, cactus1_x - 30, cactus1_y + 60),
            270,
            90,
            fill=0,
            width=3,
        )
        # 右臂
        draw.line((cactus1_x + 20, cactus1_y + 80, cactus1_x + 45, cactus1_y + 80), fill=0, width=3)
        draw.line((cactus1_x + 45, cactus1_y + 80, cactus1_x + 45, cactus1_y + 50), fill=0, width=3)
        draw.arc(
            (cactus1_x + 25, cactus1_y + 50, cactus1_x + 65, cactus1_y + 90),
            90,
            270,
            fill=0,
            width=3,
        )

        # 小仙人掌（圆形）
        cactus2_x = 500
        cactus2_y = horizon_y - 60
        draw.ellipse(
            (cactus2_x - 30, cactus2_y - 50, cactus2_x + 30, cactus2_y + 10), outline=0, width=3
        )
        # 花
        draw.ellipse((cactus2_x - 10, cactus2_y - 60, cactus2_x + 10, cactus2_y - 40), fill=0)

        # 骷髅头（装饰）
        skull_x = 600
        skull_y = horizon_y - 40
        # 头骨
        draw.ellipse((skull_x - 25, skull_y - 30, skull_x + 25, skull_y + 10), outline=0, width=2)
        # 眼睛
        draw.ellipse((skull_x - 15, skull_y - 20, skull_x - 5, skull_y - 10), fill=0)
        draw.ellipse((skull_x + 5, skull_y - 20, skull_x + 15, skull_y - 10), fill=0)
        # 鼻子
        draw.polygon(
            [(skull_x - 5, skull_y - 5), (skull_x, skull_y + 5), (skull_x + 5, skull_y - 5)], fill=0
        )
