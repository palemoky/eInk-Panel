"""Tests for Weather provider."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.exceptions import ProviderError
from src.providers.weather import get_weather


class TestWeatherProvider:
    """Tests for weather provider functions."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_get_weather_success(self, mock_client):
        """Test successful weather fetch."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"main": {"temp": 25.5}, "weather": [{"main": "Clouds"}]}
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response

        # Set API key
        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key", "CITY_NAME": "TestCity"}):
            # Reload config to pick up env vars
            from src import config

            config.Config.reload()

            data = await get_weather(mock_client)

            assert data["temp"] == "25.5"
            assert data["desc"] == "Clouds"
            assert data["icon"] == "Clouds"

            # Verify API call
            mock_client.get.assert_called_once()
            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["q"] == "TestCity"
            assert call_args[1]["params"]["appid"] == "test_key"

    @pytest.mark.asyncio
    async def test_get_weather_no_api_key(self, mock_client):
        """Test fallback when API key is missing."""
        # Unset API key
        with patch.dict(os.environ, {}, clear=True):
            # Restore other potentially needed env vars if any, but ensure OPENWEATHER_API_KEY is gone
            if "OPENWEATHER_API_KEY" in os.environ:
                del os.environ["OPENWEATHER_API_KEY"]

            from src import config

            config.Config.reload()

            data = await get_weather(mock_client)

            # Should return fallback data
            assert data["temp"] == "13.9"
            assert data["desc"] == "Sunny"
            assert data["icon"] == "Clear"

            # Should not make API call
            mock_client.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_weather_api_error(self, mock_client):
        """Test handling of API errors."""
        # Mock API error
        mock_client.get.side_effect = httpx.HTTPError("API Error")

        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            with pytest.raises(ProviderError) as exc:
                await get_weather(mock_client)

            assert "Failed to fetch weather data" in str(exc.value)
            assert exc.value.provider == "weather"

    @pytest.mark.asyncio
    async def test_get_weather_unexpected_error(self, mock_client):
        """Test handling of unexpected errors."""
        # Mock unexpected error
        mock_client.get.side_effect = Exception("Unexpected")

        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            with pytest.raises(ProviderError) as exc:
                await get_weather(mock_client)

            assert "Unexpected error" in str(exc.value)
            assert exc.value.provider == "weather"
