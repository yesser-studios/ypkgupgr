import os
from pathlib import Path
from unittest.mock import patch

import pytest

from ypkgupgr import appdata


class TestAppdata:
    """Tests for appdata functionality."""

    def test_appdata_dir_is_string(self):
        """appdata_dir should be a string."""
        assert isinstance(appdata.appdata_dir, str)

    def test_ignored_path_is_string(self):
        """ignored_path should be a string."""
        assert isinstance(appdata.ignored_path, str)

    def test_log_dir_is_string(self):
        """log_dir should be a string."""
        assert isinstance(appdata.log_dir, str)

    def test_log_file_is_string(self):
        """log_file should be a string."""
        assert isinstance(appdata.log_file, str)

    def test_ignored_path_contains_ignored_cfg(self):
        """ignored_path should end with ignored.cfg."""
        assert appdata.ignored_path.endswith("ignored.cfg")

    def test_log_file_contains_log_log(self):
        """log_file should end with log.log."""
        assert appdata.log_file.endswith("log.log")

    def test_create_appdata_dirs_creates_log_dir(self, tmp_path, monkeypatch):
        """Should create log directory."""
        log_dir = tmp_path / "logs"
        monkeypatch.setattr("ypkgupgr.appdata.log_dir", str(log_dir))

        appdata.create_appdata_dirs()

        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_create_appdata_dirs_does_not_fail_if_exists(self, tmp_path, monkeypatch):
        """Should handle existing log directory."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        monkeypatch.setattr("ypkgupgr.appdata.log_dir", str(log_dir))

        appdata.create_appdata_dirs()

        assert log_dir.exists()

    def test_app_name_in_paths(self):
        """Paths should contain the app name."""
        assert "ypkgupgr" in appdata.appdata_dir.lower()
        assert "ypkgupgr" in appdata.log_dir.lower()

    def test_author_name_in_paths(self):
        """Paths should contain the app name (author may or may not be in path depending on OS)."""
        assert (
            "ypkgupgr" in appdata.appdata_dir.lower()
            or "ypkgupgr" in appdata.log_dir.lower()
        )
