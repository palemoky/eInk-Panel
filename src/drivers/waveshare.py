import importlib
import logging

from PIL import Image

logger = logging.getLogger(__name__)


class WaveshareEPDDriver:
    def __init__(self, model_name: str):
        """
        初始化 Waveshare 驱动适配器
        :param model_name: 驱动模块名称，例如 'epd7in5_V2'
        """
        try:
            # 动态导入 src.lib.waveshare_epd.{model_name}
            module_path = f"src.lib.waveshare_epd.{model_name}"
            self.epd_module = importlib.import_module(module_path)

            # 实例化 EPD 类
            self.epd = self.epd_module.EPD()
            self.width = self.epd.width
            self.height = self.epd.height
            logger.info(f"Loaded Waveshare driver: {model_name} ({self.width}x{self.height})")

        except ImportError as e:
            logger.error(f"Failed to load Waveshare driver '{model_name}': {e}")
            raise
        except AttributeError as e:
            logger.error(
                f"Driver '{model_name}' does not have expected EPD class or attributes: {e}"
            )
            raise

    def init(self, fast: bool = False) -> None:
        """Initialize the display.

        Args:
            fast: If True, use fast refresh mode (less flashing but may have ghosting).
                  If False, use full refresh mode (more flashing but better quality).
        """
        if fast and hasattr(self.epd, "init_fast"):
            logger.debug("Using fast refresh mode")
            self.epd.init_fast()
        else:
            logger.debug("Using full refresh mode")
            self.epd.init()

    def clear(self) -> None:
        self.epd.Clear()

    def sleep(self) -> None:
        self.epd.sleep()

    def display(self, image: Image.Image) -> None:
        # Waveshare 驱动通常需要 getbuffer
        buffer = self.epd.getbuffer(image)
        self.epd.display(buffer)
