from ypkgupgr import appdata


class TestIgnoredIntegration:
    """Integration tests for ignore/unignore functionality."""

    def test_ignored_file_path_exists(self):
        """Verify ignored_path is defined in appdata."""
        assert hasattr(appdata, "ignored_path")
        assert isinstance(appdata.ignored_path, str)
        assert "ignored" in appdata.ignored_path.lower()
