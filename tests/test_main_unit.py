import sys
from unittest.mock import patch

import pytest


class TestMainUnit:
    """Unit tests for main module functions."""

    def test_get_python_executable_with_venv_path(self, tmp_path, monkeypatch):
        """get_python_executable should use specified venv path."""
        import ypkgupgr

        venv_path = tmp_path / "venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        monkeypatch.setattr("ypkgupgr.get_venv_python", lambda x: python_path)

        result = ypkgupgr.get_python_executable(venv_path=str(venv_path))

        assert result == str(python_path)

    def test_get_python_executable_invalid_venv_raises(self, monkeypatch):
        """get_python_executable with invalid venv should raise."""
        import click
        import ypkgupgr

        monkeypatch.setattr("ypkgupgr.get_venv_python", lambda x: None)

        with pytest.raises(
            click.ClickException, match="Invalid virtual environment path"
        ):
            ypkgupgr.get_python_executable(venv_path="/invalid/path")

    def test_check_ypkgupgr_script_returns_false_on_non_windows(self, monkeypatch):
        """check_ypkgupgr_script should return False on non-Windows."""
        import ypkgupgr

        monkeypatch.setattr(sys, "platform", "linux")

        result = ypkgupgr.check_ypkgupgr_script("ypkgupgr", 0)

        assert result is False

    def test_check_ypkgupgr_script_returns_false_for_non_ypkgupgr(self, monkeypatch):
        """check_ypkgupgr_script should return False for non-ypkgupgr packages."""
        import ypkgupgr
        import ypkgupgr.misc as misc_module

        monkeypatch.setattr(sys, "platform", "win32")
        monkeypatch.setattr(misc_module, "ran_from_script", True)

        result = ypkgupgr.check_ypkgupgr_script("otherpkg", 0)

        assert result is False

    def test_start_updates_sync_iterates_packages(self, monkeypatch):
        """start_updates_sync should iterate through packages."""
        import ypkgupgr

        lines = ["package1 1.0.0 2.0.0", "package2 1.0.0 2.0.0"]

        with patch("ypkgupgr.update_sync") as mock_update:
            ypkgupgr.start_updates_sync(lines)

            assert mock_update.call_count == 2

    def test_main_module_imports(self):
        """Verify the main module can be imported and has expected functions."""
        import ypkgupgr

        assert hasattr(ypkgupgr, "get_python_executable")
        assert hasattr(ypkgupgr, "check_ignored")
        assert hasattr(ypkgupgr, "check_ypkgupgr_script")
        assert hasattr(ypkgupgr, "post_update")
        assert hasattr(ypkgupgr, "update")
        assert hasattr(ypkgupgr, "update_sync")
        assert hasattr(ypkgupgr, "start_updates")
        assert hasattr(ypkgupgr, "start_updates_sync")
        assert hasattr(ypkgupgr, "update_packages")
        assert hasattr(ypkgupgr, "update_command")
