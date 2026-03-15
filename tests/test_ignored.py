import os
import subprocess
import sys
import tempfile
from pathlib import Path


class TestIgnoredIntegration:
    """Integration tests for ignore/unignore functionality via CLI."""

    def test_ignore_creates_file(self, tmp_path):
        """Should create ignored file with package names."""
        ignored_file = tmp_path / "ignored.cfg"

        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "ignore", "testpkg", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_unignore_removes_package(self, tmp_path):
        """Should remove package from ignored file."""
        ignored_file = tmp_path / "ignored.cfg"
        ignored_file.write_text("package1\npackage2\n")

        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore", "package1", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_unignore_all_clears_file(self, tmp_path):
        """Should clear the ignored file."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore-all", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ignored_file_path_exists(self):
        """Verify ignored_path is defined in appdata."""
        from ypkgupgr import appdata

        assert hasattr(appdata, "ignored_path")
        assert isinstance(appdata.ignored_path, str)
        assert "ignored" in appdata.ignored_path.lower()
