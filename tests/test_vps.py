"""Tests for VPS provider."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.exceptions import ProviderError
from src.providers.vps import get_vps_info


class TestVPSProvider:
    """Tests for VPS provider functions."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_get_vps_info_success(self, mock_client):
        """Test successful VPS info fetch."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": 0,
            "data_counter": 500,
            "plan_monthly_data": 1000,
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response

        # Set API key
        with patch.dict(os.environ, {"VPS_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            usage = await get_vps_info(mock_client)

            assert usage == 50

            # Verify API call
            mock_client.get.assert_called_once()
            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["veid"] == "test_key"

    @pytest.mark.asyncio
    async def test_get_vps_info_no_api_key(self, mock_client):
        """Test fallback when API key is missing."""
        # Unset API key
        with patch.dict(os.environ, {}, clear=True):
            if "VPS_API_KEY" in os.environ:
                del os.environ["VPS_API_KEY"]

            from src import config

            config.Config.reload()

            usage = await get_vps_info(mock_client)

            assert usage == 0
            mock_client.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_vps_info_api_error_response(self, mock_client):
        """Test handling of API error response (error != 0)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": 1}
        mock_client.get.return_value = mock_response

        with patch.dict(os.environ, {"VPS_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            usage = await get_vps_info(mock_client)

            assert usage == 0

    @pytest.mark.asyncio
    async def test_get_vps_info_http_error(self, mock_client):
        """Test handling of HTTP errors."""
        mock_client.get.side_effect = httpx.HTTPError("API Error")

        with patch.dict(os.environ, {"VPS_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            with pytest.raises(ProviderError) as exc:
                await get_vps_info(mock_client)

            assert "Failed to fetch VPS info" in str(exc.value)

    @pytest.mark.asyncio
    async def test_get_vps_info_unexpected_error(self, mock_client):
        """Test handling of unexpected errors."""
        mock_client.get.side_effect = Exception("Unexpected")

        with patch.dict(os.environ, {"VPS_API_KEY": "test_key"}):
            from src import config

            config.Config.reload()

            with pytest.raises(ProviderError) as exc:
                await get_vps_info(mock_client)

            assert "Unexpected error" in str(exc.value)
