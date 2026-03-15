import pytest
from ypkgupgr.colors import Colors


class TestColors:
    """Tests for color constants."""

    def test_white_is_ansi_escape(self):
        """White should be a valid ANSI escape sequence."""
        assert Colors.WHITE.startswith("\033[")
        assert "37" in Colors.WHITE

    def test_red_is_ansi_escape(self):
        """Red should be a valid ANSI escape sequence."""
        assert Colors.RED.startswith("\033[")
        assert "31" in Colors.RED

    def test_yellow_is_ansi_escape(self):
        """Yellow should be a valid ANSI escape sequence."""
        assert Colors.YELLOW.startswith("\033[")
        assert "33" in Colors.YELLOW

    def test_green_is_ansi_escape(self):
        """Green should be a valid ANSI escape sequence."""
        assert Colors.GREEN.startswith("\033[")
        assert "32" in Colors.GREEN

    def test_reset_is_ansi_escape(self):
        """Reset should be a valid ANSI escape sequence."""
        assert Colors.RESET.startswith("\033[")
        assert "0" in Colors.RESET

    def test_all_colors_are_strings(self):
        """All color constants should be strings."""
        assert isinstance(Colors.WHITE, str)
        assert isinstance(Colors.RED, str)
        assert isinstance(Colors.YELLOW, str)
        assert isinstance(Colors.GREEN, str)
        assert isinstance(Colors.RESET, str)

    def test_colors_are_not_empty(self):
        """All color constants should be non-empty."""
        assert Colors.WHITE
        assert Colors.RED
        assert Colors.YELLOW
        assert Colors.GREEN
        assert Colors.RESET
