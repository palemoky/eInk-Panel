"""Tests for PoetryLayout."""

from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from src.layouts.poetry import PoetryLayout


class TestPoetryLayout:
    """Tests for PoetryLayout class."""

    @pytest.fixture
    def layout(self):
        """Create a PoetryLayout instance."""
        with patch("src.layouts.poetry.DashboardRenderer"):
            return PoetryLayout()

    def test_init(self, layout):
        """Test initialization."""
        assert layout.renderer is not None
        assert layout.font_path is not None
        assert layout.seal_font_path is not None

    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_create_poetry_image_empty(self, mock_font, layout):
        """Test creating image with empty data."""
        image = layout.create_poetry_image(800, 480, {})
        assert isinstance(image, Image.Image)
        assert image.size == (800, 480)

    @patch("src.layouts.poetry.ImageDraw.Draw")
    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_create_poetry_image_basic(self, mock_font, mock_draw_cls, layout):
        """Test creating image with basic poetry data."""
        poetry = {
            "content": "床前明月光，疑是地上霜。\n举头望明月，低头思故乡。",
            "author": "李白",
            "source": "静夜思",
        }

        # Setup mock draw
        mock_draw = MagicMock()
        mock_draw_cls.return_value = mock_draw
        mock_draw.textbbox.return_value = (0, 0, 20, 20)

        image = layout.create_poetry_image(800, 480, poetry)

        assert isinstance(image, Image.Image)
        # Verify text was drawn
        assert mock_draw.text.called

    @patch("src.layouts.poetry.ImageDraw.Draw")
    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_create_poetry_image_list_content(self, mock_font, mock_draw_cls, layout):
        """Test creating image with list content."""
        poetry = {
            "content": ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"],
            "author": "李白",
            "source": "静夜思",
        }

        mock_draw = MagicMock()
        mock_draw_cls.return_value = mock_draw
        mock_draw.textbbox.return_value = (0, 0, 20, 20)

        image = layout.create_poetry_image(800, 480, poetry)
        assert isinstance(image, Image.Image)
        assert mock_draw.text.called

    @patch("src.layouts.poetry.ImageDraw.Draw")
    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_create_poetry_image_long_title(self, mock_font, mock_draw_cls, layout):
        """Test creating image with long title."""
        poetry = {
            "content": "test",
            "author": "Author",
            "source": "Very Long Title That Needs Split",
        }

        mock_draw = MagicMock()
        mock_draw_cls.return_value = mock_draw
        mock_draw.textbbox.return_value = (0, 0, 20, 20)

        image = layout.create_poetry_image(800, 480, poetry)
        assert isinstance(image, Image.Image)
        assert mock_draw.text.called

    @patch("src.layouts.poetry.ImageDraw.Draw")
    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_create_poetry_image_cipai(self, mock_font, mock_draw_cls, layout):
        """Test creating image with Cipai (· separator)."""
        poetry = {
            "content": "test",
            "author": "Author",
            "source": "Cipai·Title",
        }

        mock_draw = MagicMock()
        mock_draw_cls.return_value = mock_draw
        mock_draw.textbbox.return_value = (0, 0, 20, 20)

        image = layout.create_poetry_image(800, 480, poetry)
        assert isinstance(image, Image.Image)
        assert mock_draw.text.called

    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_draw_seal_2_chars(self, mock_font, layout):
        """Test drawing seal with 2 characters."""
        draw = MagicMock()

        layout._draw_seal(draw, "李白", 0, 0, 50)

        # Verify text calls
        assert draw.text.call_count >= 4

    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_draw_seal_3_chars(self, mock_font, layout):
        """Test drawing seal with 3 characters."""
        draw = MagicMock()

        layout._draw_seal(draw, "王维印", 0, 0, 50)

        assert draw.text.call_count >= 4

    @patch("src.layouts.poetry.ImageFont.truetype")
    def test_draw_seal_4_chars(self, mock_font, layout):
        """Test drawing seal with 4 characters."""
        draw = MagicMock()

        layout._draw_seal(draw, "欧阳修印", 0, 0, 50)

        assert draw.text.call_count >= 4

    def test_draw_decorative_corners(self, layout):
        """Test drawing decorative corners."""
        draw = MagicMock()

        layout._draw_decorative_corners(draw, 800, 480)

        # Verify line calls (4 corners * 2 lines = 8 lines)
        assert draw.line.call_count == 8
