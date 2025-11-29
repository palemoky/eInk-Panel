"""Tests for DataFetcher."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.data_fetcher import DataFetcher
from src.providers import Dashboard


class TestDataFetcher:
    """Tests for DataFetcher class."""

    @pytest.fixture
    def mock_dashboard(self):
        """Create a mock dashboard provider."""
        dashboard = MagicMock(spec=Dashboard)
        dashboard.client = AsyncMock()
        dashboard.fetch_dashboard_data = AsyncMock(return_value={"test": "data"})
        dashboard.fetch_year_end_data = AsyncMock(return_value={"year": "end"})
        return dashboard

    @pytest.fixture
    def fetcher(self, mock_dashboard):
        """Create a DataFetcher instance."""
        return DataFetcher(mock_dashboard)

    @pytest.mark.asyncio
    async def test_fetch_dashboard(self, fetcher, mock_dashboard):
        """Test fetching dashboard data."""
        data = await fetcher.fetch("dashboard")

        assert data == {"test": "data"}
        mock_dashboard.fetch_dashboard_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_quote(self, fetcher):
        """Test fetching quote data."""
        with patch("src.providers.quote.get_quote", new_callable=AsyncMock) as mock_get_quote:
            mock_get_quote.return_value = "Test Quote"

            data = await fetcher.fetch("quote")

            assert data == {"quote": "Test Quote"}
            mock_get_quote.assert_called_once_with(fetcher.dashboard.client)

    @pytest.mark.asyncio
    async def test_fetch_poetry(self, fetcher):
        """Test fetching poetry data."""
        with patch("src.providers.poetry.get_poetry", new_callable=AsyncMock) as mock_get_poetry:
            mock_get_poetry.return_value = "Test Poetry"

            data = await fetcher.fetch("poetry")

            assert data == {"poetry": "Test Poetry"}
            mock_get_poetry.assert_called_once_with(fetcher.dashboard.client)

    @pytest.mark.asyncio
    async def test_fetch_wallpaper(self, fetcher):
        """Test fetching wallpaper data."""
        data = await fetcher.fetch("wallpaper")
        assert data == {}

    @pytest.mark.asyncio
    async def test_fetch_holiday(self, fetcher):
        """Test fetching holiday data."""
        with patch("src.layouts.holiday.HolidayManager") as MockHolidayManager:
            mock_manager = MockHolidayManager.return_value
            mock_manager.get_holiday.return_value = "Christmas"

            data = await fetcher.fetch("holiday")

            assert data == {"holiday": "Christmas"}
            mock_manager.get_holiday.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_year_end(self, fetcher, mock_dashboard):
        """Test fetching year-end data."""
        data = await fetcher.fetch("year_end")

        assert data == {"year": "end"}
        mock_dashboard.fetch_year_end_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_unknown_mode(self, fetcher, mock_dashboard):
        """Test fetching unknown mode defaults to dashboard."""
        data = await fetcher.fetch("unknown_mode")

        assert data == {"test": "data"}
        mock_dashboard.fetch_dashboard_data.assert_called_once()
