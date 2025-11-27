import logging

from PIL import Image

logger = logging.getLogger(__name__)


class MockEPDDriver:
    def __init__(self, width: int = 800, height: int = 480):
        self.width = width
        self.height = height
        logger.info(f"Mock EPD initialized with size {width}x{height}")

    def init(self, fast: bool = False) -> None:
        refresh_mode = "fast" if fast else "full"
        logger.info(f"Mock EPD: init ({refresh_mode} refresh)")

    def clear(self) -> None:
        logger.info("Mock EPD: clear")

    def sleep(self) -> None:
        logger.info("Mock EPD: sleep")

    def display(self, image: Image.Image) -> None:
        logger.info(f"Mock EPD: display image size={image.size}")
        # 调试模式下保存图片
        try:
            image.save("mock_display_output.png")
            logger.info("Saved mock display output to mock_display_output.png")
        except Exception as e:
            logger.warning(f"Failed to save mock output: {e}")
