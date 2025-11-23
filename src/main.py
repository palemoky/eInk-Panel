import asyncio
import logging
import os
import signal
import sys

import pendulum

# 支持直接运行和作为模块运行
try:
    from .config import Config
    from .data_manager import DataManager
    from .drivers.factory import get_driver
    from .layout import DashboardLayout
except ImportError:
    # 如果相对导入失败，添加父目录到路径并使用绝对导入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import Config
    from src.data_manager import DataManager
    from src.drivers.factory import get_driver
    from src.layout import DashboardLayout

# 配置日志（支持环境变量控制日志级别）
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# 全局变量用于信号处理
_driver = None


def signal_handler(signum, frame):
    """处理 SIGTERM/SIGINT 信号，确保优雅关闭"""
    logger.info(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    if _driver:
        try:
            logger.info("Putting display to sleep...")
            _driver.sleep()
            logger.info("✅ Display sleep successful")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    sys.exit(0)


# 注册信号处理器
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def is_in_quiet_hours():
    """检查当前时间是否在静默时间段内，并返回需要休眠的秒数"""
    now = pendulum.now(Config.TIMEZONE)

    # 构建今天的开始和结束时间点
    start_time = now.replace(hour=Config.QUIET_START_HOUR, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=Config.QUIET_END_HOUR, minute=0, second=0, microsecond=0)

    # 处理跨天的情况 (例如 23:00 到 06:00)
    if Config.QUIET_START_HOUR > Config.QUIET_END_HOUR:
        if now.hour >= Config.QUIET_START_HOUR:
            # 现在是晚上，结束时间是明天
            end_time = end_time.add(days=1)
        elif now.hour < Config.QUIET_END_HOUR:
            # 现在是凌晨，开始时间是昨天
            start_time = start_time.subtract(days=1)

    # 判断是否在范围内
    if start_time <= now < end_time:
        sleep_seconds = (end_time - now).total_seconds()
        return True, int(sleep_seconds)

    return False, 0


async def main():
    """主函数"""
    global _driver

    # 验证必需的环境变量
    try:
        Config.validate_required()
    except ValueError as e:
        logger.error(str(e))
        return

    logger.info("Starting E-Ink Panel Dashboard...")
    logger.info(f"Refresh interval: {Config.REFRESH_INTERVAL}s")
    logger.info(f"Quiet hours: {Config.QUIET_START_HOUR}:00 - {Config.QUIET_END_HOUR}:00")

    # 初始化驱动
    _driver = get_driver()
    epd = _driver  # 保持局部变量以兼容现有代码

    layout = DashboardLayout()

    # 使用 DataManager 上下文管理器 (管理 HTTP Client)
    async with DataManager() as dm:
        try:
            # 首次启动执行一次完整清屏
            logger.info("Performing initial clear...")
            epd.init()
            epd.clear()
            epd.sleep()

            while True:
                now = pendulum.now(Config.TIMEZONE)
                current_time = now.to_time_string()

                # 检查是否在静默时间段
                in_quiet, sleep_seconds = is_in_quiet_hours()
                if in_quiet:
                    logger.info(
                        f"In quiet hours ({Config.QUIET_START_HOUR}:00-{Config.QUIET_END_HOUR}:00), sleeping for {sleep_seconds} seconds"
                    )
                    await asyncio.sleep(sleep_seconds)
                    continue

                logger.info(f"Refreshing at {current_time}")

                # 检查是否启用壁纸模式
                if Config.WALLPAPER_MODE:
                    from .wallpaper import WallpaperManager

                    wallpaper_manager = WallpaperManager()
                    wallpaper_name = Config.WALLPAPER_NAME if Config.WALLPAPER_NAME else None
                    image = wallpaper_manager.create_wallpaper(
                        epd.width, epd.height, wallpaper_name
                    )
                    logger.info(f"🎨 Wallpaper mode: {wallpaper_name or 'random'}")
                else:
                    # 正常模式：获取数据并生成图像
                    # 1. 并发获取数据
                    data = await dm.fetch_all_data()

                    # 2. 生成图像
                    image = layout.create_image(epd.width, epd.height, data)

                if Config.IS_SCREENSHOT_MODE:
                    image.save(Config.DATA_DIR / "screenshot.bmp")
                    logger.info("Saved screenshot.bmp")

                # 3. 显示到屏幕
                # 关键优化：遵循 Init -> Display -> Sleep 流程保护屏幕
                logger.info("Updating display...")
                epd.init()
                epd.display(image)
                epd.sleep()
                logger.info("Display updated and put to sleep.")

                # 4. 检查是否是节日
                from .holiday import HolidayManager

                holiday_manager = HolidayManager()
                holiday = holiday_manager.get_holiday()

                if holiday:
                    # 如果是节日，显示祝福后等到第二天再刷新
                    logger.info(f"🎉 Today is {holiday['name']}! Displaying greeting all day.")
                    # 计算到明天凌晨的秒数
                    tomorrow = now.add(days=1).start_of("day")
                    sleep_until_tomorrow = (tomorrow - now).total_seconds()
                    logger.info(f"Sleeping until tomorrow ({sleep_until_tomorrow:.0f}s)")
                    await asyncio.sleep(sleep_until_tomorrow)
                else:
                    # 正常刷新间隔
                    await asyncio.sleep(Config.REFRESH_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Exiting...")
            epd.init()
            epd.Clear()
            epd.sleep()
        except Exception as e:
            logger.error(f"Critical Error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
