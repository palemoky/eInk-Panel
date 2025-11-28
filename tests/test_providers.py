"""Tests for data providers and API integrations."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.providers.dashboard import get_github_commits, get_weather


@pytest.mark.asyncio
async def test_get_weather_success():
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {"temp": 20.5},
        "weather": [{"main": "Clouds"}],
    }
    mock_response.raise_for_status = MagicMock()

    # Mock client
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    # Set API key temporarily - patch the grouped config
    with patch("src.config.Config.api.openweather_api_key", "fake_key"):
        data = await get_weather(mock_client)

    assert data["temp"] == "20.5"
    assert data["desc"] == "Clouds"
    assert data["icon"] == "Clouds"


@pytest.mark.asyncio
async def test_get_github_commits_fail():
    # Simulate network error
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.side_effect = httpx.RequestError("Network Down", request=MagicMock())

    # Patch the grouped config
    with (
        patch("src.config.Config.github.username", "testuser"),
        patch("src.config.Config.github.token", "fake_token"),
    ):
        # Function should return zeroed dict on error, not raise exception
        result = await get_github_commits(mock_client)
        assert result == {"day": 0, "month": 0, "year": 0}
