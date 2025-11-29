"""Tests for data providers and API integrations."""

import os
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from src.providers.btc import get_btc_data
from src.providers.dashboard import get_github_commits


@pytest.mark.asyncio
async def test_get_btc_success():
    """Test successful BTC price fetch."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"bitcoin": {"usd": 50000, "usd_24h_change": 2.5}}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    data = await get_btc_data(mock_client)
    assert data == {"usd": 50000, "usd_24h_change": 2.5}


@pytest.mark.asyncio
async def test_get_github_commits_no_credentials():
    """Test GitHub commits with no credentials returns zero dict."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)

    # Temporarily unset credentials
    old_username = os.environ.get("GITHUB_USERNAME")
    old_token = os.environ.get("GITHUB_TOKEN")

    try:
        if "GITHUB_USERNAME" in os.environ:
            del os.environ["GITHUB_USERNAME"]
        if "GITHUB_TOKEN" in os.environ:
            del os.environ["GITHUB_TOKEN"]

        # Reload config
        from src import config

        config.Config.model_rebuild()

        result = await get_github_commits(mock_client)
        assert result == {"day": 0, "week": 0, "month": 0, "year": 0}
    finally:
        # Restore
        if old_username:
            os.environ["GITHUB_USERNAME"] = old_username
        if old_token:
            os.environ["GITHUB_TOKEN"] = old_token
        from src import config

        config.Config.model_rebuild()
