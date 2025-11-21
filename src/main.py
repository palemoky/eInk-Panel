import sys
import os
import time
import logging

# 支持直接运行和作为模块运行
try:
    from .config import Config
    from .layout import DashboardLayout
except ImportError:
    # 如果相对导入失败，添加父目录到路径并使用绝对导入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import Config
    from src.layout import DashboardLayout

# Fix import path for drivers
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# 配置日志（在导入 EPD 之前）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info(f"Adding lib path: {lib_path}")
logger.info(f"lib path exists: {os.path.exists(lib_path)}")

# Mock driver if running on PC (Optional)
try:
    from epd7in5_V2 import EPD
    logger.info("EPD driver loaded successfully!")
except ImportError as e:
    logger.warning(f"EPD driver not found ({e}), using mock.")

    class EPD:
        width, height = 800, 480

        def init(self):
            pass

        def Clear(self):
            pass

        def display(self, buf):
            pass

        def getbuffer(self, img):
            return None

        def sleep(self):
            pass



def is_in_quiet_hours():
    """检查当前时间是否在静默时间段内，并返回需要休眠的秒数
    
    Returns:
        tuple: (是否在静默时间段, 需要休眠的秒数)
    """
    import pendulum
    
    now = pendulum.now()
    
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


def main():
    logger.info("Starting Dashboard...")
    epd = EPD()
    layout = DashboardLayout()

    try:
        epd.init()
        epd.Clear()

        while True:
            current_time = time.strftime('%H:%M:%S')
            
            # 检查是否在静默时间段
            in_quiet, sleep_seconds = is_in_quiet_hours()
            if in_quiet:
                logger.info(f"In quiet hours ({Config.QUIET_START_HOUR}:00-{Config.QUIET_END_HOUR}:00), sleeping for {sleep_seconds} seconds until {Config.QUIET_END_HOUR}:00")
                time.sleep(sleep_seconds)
                continue
            
            logger.info(f"Refreshing at {current_time}")

            # Generate Image
            img = layout.create_image(epd.width, epd.height)

            if Config.IS_SCREENSHOT_MODE:
                img.save("screenshot.bmp")
                logger.info("Saved screenshot.bmp")

            # Display
            epd.display(epd.getbuffer(img))

            time.sleep(Config.REFRESH_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Exiting...")
        epd.init()
        epd.Clear()
        epd.sleep()
    except Exception as e:
        logger.error(f"Critical Error: {e}", exc_info=True)


if __name__ == "__main__":
    main()

