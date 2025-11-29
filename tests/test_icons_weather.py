"""Tests for WeatherIcons."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from src.renderer.icons.weather import WeatherIcons


class TestWeatherIcons:
    """Tests for WeatherIcons class."""

    @pytest.fixture
    def icons(self):
        """Create WeatherIcons instance."""
        return WeatherIcons()

    @pytest.fixture
    def mock_draw(self):
        """Create mock ImageDraw."""
        draw = MagicMock()
        # Mock internal image for paste operations
        draw._image = MagicMock()
        return draw

    def test_draw_weather_icon_from_file(self, icons, mock_draw, tmp_path):
        """Test loading icon from file."""
        # Create a dummy icon file
        icon_path = tmp_path / "sun.png"
        img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        img.save(icon_path)

        result = icons.draw_weather_icon(mock_draw, 100, 100, "sun", size=30, icons_dir=tmp_path)

        assert result is True
        mock_draw._image.paste.assert_called()

    def test_draw_weather_icon_fallback(self, icons, mock_draw):
        """Test fallback to code drawing when file missing."""
        # Use non-existent directory
        result = icons.draw_weather_icon(
            mock_draw, 100, 100, "sun", size=30, icons_dir=Path("/non/existent")
        )

        assert result is False
        # Should have called draw_sun which uses ellipse/line
        assert mock_draw.ellipse.called or mock_draw.line.called

    def test_draw_sun(self, icons, mock_draw):
        """Test drawing sun icon."""
        icons.draw_sun(mock_draw, 100, 100, 30)
        assert mock_draw.ellipse.called
        assert mock_draw.line.called

    def test_draw_cloud(self, icons, mock_draw):
        """Test drawing cloud icon."""
        icons.draw_cloud(mock_draw, 100, 100, 30)
        assert mock_draw.ellipse.call_count >= 3
        assert mock_draw.rectangle.called

    def test_draw_rain(self, icons, mock_draw):
        """Test drawing rain icon."""
        icons.draw_rain(mock_draw, 100, 100, 30)
        # Should draw cloud + rain lines
        assert mock_draw.ellipse.called
        assert mock_draw.line.called

    def test_draw_snow(self, icons, mock_draw):
        """Test drawing snow icon."""
        icons.draw_snow(mock_draw, 100, 100, 30)
        # Should draw cloud + snow circles
        assert mock_draw.ellipse.called

    def test_draw_thunder(self, icons, mock_draw):
        """Test drawing thunder icon."""
        icons.draw_thunder(mock_draw, 100, 100, 30)
        # Should draw cloud + lightning lines
        assert mock_draw.ellipse.called
        assert mock_draw.line.called

    def test_draw_unknown_icon(self, icons, mock_draw):
        """Test drawing unknown icon defaults to cloud."""
        with patch.object(icons, "draw_cloud") as mock_draw_cloud:
            icons.draw_weather_icon(mock_draw, 100, 100, "unknown_icon")
            mock_draw_cloud.assert_called_once()
