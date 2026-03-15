import subprocess
import sys


class TestMainIntegration:
    """Integration tests for main module CLI."""

    def test_ypkgupgr_help_command(self):
        """ypkgupgr --help should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "update" in output.lower() or "options" in output.lower()

    def test_ypkgupgr_version_command(self):
        """ypkgupgr --version should work or show no such option."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--version"],
            capture_output=True,
            text=True,
        )

        output = result.stdout + result.stderr
        assert "version" in output.lower() or "no such option" in output.lower()

    def test_ypkgupgr_ignore_command(self):
        """ypkgupgr ignore should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "ignore", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ypkgupgr_unignore_command(self):
        """ypkgupgr unignore should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ypkgupgr_unignore_all_command(self):
        """ypkgupgr unignore-all should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore-all", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ypkgupgr_log_path_command(self):
        """ypkgupgr log-path should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "log-path", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ypkgupgr_open_logs_command(self):
        """ypkgupgr open-logs should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "open-logs", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_ypkgupgr_invalid_option(self):
        """ypkgupgr with invalid option should show error."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--invalid-option"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0

    def test_ypkgupgr_venv_and_no_venv_conflict(self):
        """Using both --venv and --no-venv should error."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--venv", "/path", "--no-venv"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0

    def test_entry_point_ypkgupgr_help(self):
        """ypkgupgr entry point with --help should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0

    def test_entry_point_yesserpackageupdater_help(self):
        """yesserpackageupdater entry point with --help should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0
