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
    import datetime
    
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_second = now.second
    
    start = Config.QUIET_START_HOUR
    end = Config.QUIET_END_HOUR
    
    # 判断是否在静默时间段
    in_quiet = False
    if start < end:
        in_quiet = start <= current_hour < end
    else:
        in_quiet = current_hour >= start or current_hour < end
    
    if not in_quiet:
        return False, 0
    
    # 计算到静默时间段结束还需要多少秒
    end_time = now.replace(hour=end, minute=0, second=0, microsecond=0)
    
    # 如果结束时间小于当前时间，说明结束时间是明天
    if end_time <= now:
        end_time += datetime.timedelta(days=1)
    
    sleep_seconds = (end_time - now).total_seconds()
    
    return True, int(sleep_seconds)


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

