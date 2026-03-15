import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from ypkgupgr import logs


class TestLogs:
    """Tests for logging functionality."""

    def test_logger_is_logger_instance(self):
        """Logger should be a logging.Logger instance."""
        assert isinstance(logs.logger, logging.Logger)

    def test_logger_name_is_logger(self):
        """Logger name should be 'logger'."""
        assert logs.logger.name == "logger"

    def test_init_logging_sets_level_info(self):
        """init_logging should set level to INFO by default."""
        logs.init_logging(clear_log=False, log_debug=False)
        assert logs.logger.level == logging.INFO

    def test_init_logging_sets_level_debug(self):
        """init_logging should set level to DEBUG when log_debug is True."""
        logs.init_logging(clear_log=False, log_debug=True)
        assert logs.logger.level == logging.DEBUG

    def test_init_logging_adds_file_handler(self):
        """init_logging should add a file handler."""
        logs.init_logging(clear_log=False, log_debug=False)
        assert len(logs.logger.handlers) > 0

    def test_init_logging_clears_existing_handlers(self):
        """init_logging should clear existing handlers."""
        handler = logging.FileHandler(logs.log_file)
        logs.logger.addHandler(handler)

        logs.init_logging(clear_log=False, log_debug=False)

        handler_count = sum(
            1 for h in logs.logger.handlers if isinstance(h, logging.FileHandler)
        )
        assert handler_count == 1

    def test_log_info_calls_logger_info(self):
        """log_info should call logger.info."""
        with patch.object(logs.logger, "info") as mock_info:
            logs.log_info("test message")
            mock_info.assert_called_with("test message")

    def test_log_debug_calls_logger_debug(self):
        """log_debug should call logger.debug."""
        with patch.object(logs.logger, "debug") as mock_debug:
            logs.log_debug("test message")
            mock_debug.assert_called_with("test message")

    def test_init_logging_creates_log_file(self, tmp_path, monkeypatch):
        """init_logging should create the log file."""
        log_file = tmp_path / "test.log"

        with patch("ypkgupgr.logs.log_file", str(log_file)):
            assert not log_file.exists()

            logs.init_logging(clear_log=False, log_debug=False)

            assert log_file.exists()

    def test_init_logging_with_clear_log_clears_file(self, tmp_path, monkeypatch):
        """init_logging with clear_log should clear the log file."""
        log_file = tmp_path / "test.log"
        log_file.write_text("old content")

        with patch("ypkgupgr.logs.log_file", str(log_file)):
            logs.init_logging(clear_log=True, log_debug=False)

            content = log_file.read_text()
            assert "Logger initialized" in content or content == ""

    def test_log_file_path_is_string(self):
        """log_file should be a string."""
        assert isinstance(logs.log_file, str)

    def test_log_file_path_ends_with_log_log(self):
        """log_file should end with log.log."""
        assert logs.log_file.endswith("log.log")
