import subprocess
import sys

import pytest


class TestMainIntegration:
    """Integration tests for main module CLI."""

    TIMEOUT = 30

    def test_ypkgupgr_help_command(self):
        """ypkgupgr --help should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
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
            timeout=self.TIMEOUT,
        )

        output = result.stdout + result.stderr
        if "no such option" in output.lower():
            assert result.returncode == 2
        elif "version" in output.lower():
            assert result.returncode == 0
        else:
            assert False, "Output did not match expected patterns"

    def test_ypkgupgr_ignore_command(self):
        """ypkgupgr ignore should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "ignore", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode == 0

    def test_ypkgupgr_unignore_command(self):
        """ypkgupgr unignore should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode == 0

    def test_ypkgupgr_unignore_all_command(self):
        """ypkgupgr unignore-all should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "unignore-all", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode == 0

    def test_ypkgupgr_log_path_command(self):
        """ypkgupgr log-path should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "log-path", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode == 0

    def test_ypkgupgr_open_logs_command(self):
        """ypkgupgr open-logs should work."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "open-logs", "--help"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode == 0

    def test_ypkgupgr_invalid_option(self):
        """ypkgupgr with invalid option should show error."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--invalid-option"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode != 0

    def test_ypkgupgr_venv_and_no_venv_conflict(self):
        """Using both --venv and --no-venv should error."""
        result = subprocess.run(
            [sys.executable, "-m", "ypkgupgr", "--venv", "/path", "--no-venv"],
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        assert result.returncode != 0

    def test_entry_point_ypkgupgr_help(self):
        """ypkgupgr entry point with --help should work."""
        import sys

        try:
            from importlib.metadata import entry_points
        except ImportError:
            from importlib_metadata import entry_points

        eps = entry_points()
        if hasattr(eps, "select"):
            ypkgupgr_ep = eps.select(group="console_scripts", name="ypkgupgr")
            ypkgupgr_func = next(iter(ypkgupgr_ep)).load()
        else:
            console_scripts = eps.get("console_scripts", ())
            ypkgupgr_ep = None
            for ep in console_scripts:
                if ep.name == "ypkgupgr":
                    ypkgupgr_ep = ep
                    break
            if ypkgupgr_ep is None:
                pytest.skip("ypkgupgr console script entry point not found")
            ypkgupgr_func = ypkgupgr_ep.load()

        with __import__("io").StringIO() as output:
            import sys
            from contextlib import redirect_stdout, redirect_stderr

            old_argv = sys.argv
            sys.argv = ["ypkgupgr", "--help"]
            with redirect_stdout(output), redirect_stderr(output):
                try:
                    ypkgupgr_func()
                except SystemExit:
                    pass
                finally:
                    sys.argv = old_argv
            output_value = output.getvalue()
            assert "update" in output_value.lower() or "options" in output_value.lower()
