import pytest
from ypkgupgr.consts import APP_NAME, AUTHOR_NAME


class TestConsts:
    """Tests for constants."""

    def test_app_name_is_string(self):
        """APP_NAME should be a string."""
        assert isinstance(APP_NAME, str)

    def test_app_name_is_ypkgupgr(self):
        """APP_NAME should be 'ypkgupgr'."""
        assert APP_NAME == "ypkgupgr"

    def test_author_name_is_string(self):
        """AUTHOR_NAME should be a string."""
        assert isinstance(AUTHOR_NAME, str)

    def test_author_name_is_yesser_studios(self):
        """AUTHOR_NAME should be 'Yesser Studios'."""
        assert AUTHOR_NAME == "Yesser Studios"

    def test_constants_are_not_empty(self):
        """Constants should be non-empty."""
        assert APP_NAME
        assert AUTHOR_NAME
