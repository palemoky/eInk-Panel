"""Tests for logging configuration."""

from unittest.mock import patch

from src.core.logging import (
    bind_context,
    clear_context,
    configure_logging,
    get_logger,
    unbind_context,
)


class TestLogging:
    """Tests for logging module."""

    @patch("src.core.logging.structlog")
    @patch("src.core.logging.logging")
    def test_configure_logging(self, mock_logging, mock_structlog):
        """Test logging configuration."""
        configure_logging("DEBUG")

        # Verify structlog configuration
        mock_structlog.configure.assert_called_once()

        # Verify standard logging configuration
        mock_logging.basicConfig.assert_called_once()
        call_args = mock_logging.basicConfig.call_args
        assert call_args[1]["level"] == mock_logging.DEBUG

    @patch("src.core.logging.structlog")
    def test_get_logger(self, mock_structlog):
        """Test getting a logger."""
        get_logger("test_logger")
        mock_structlog.get_logger.assert_called_once_with("test_logger")

    @patch("src.core.logging.structlog")
    def test_bind_context(self, mock_structlog):
        """Test binding context variables."""
        bind_context(user_id=123, request_id="abc")
        mock_structlog.contextvars.bind_contextvars.assert_called_once_with(
            user_id=123, request_id="abc"
        )

    @patch("src.core.logging.structlog")
    def test_unbind_context(self, mock_structlog):
        """Test unbinding context variables."""
        unbind_context("user_id", "request_id")
        mock_structlog.contextvars.unbind_contextvars.assert_called_once_with(
            "user_id", "request_id"
        )

    @patch("src.core.logging.structlog")
    def test_clear_context(self, mock_structlog):
        """Test clearing context variables."""
        clear_context()
        mock_structlog.contextvars.clear_contextvars.assert_called_once()
