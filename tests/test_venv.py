import sys
from unittest.mock import patch


class TestVenv:
    """Tests for venv detection functions."""

    def test_is_in_venv_outside_venv(self):
        """Should return False when not in a virtual environment."""
        with patch.object(sys, "prefix", sys.base_prefix):
            with patch.object(sys, "base_prefix", sys.base_prefix):
                from ypkgupgr.venv import is_in_venv

                assert is_in_venv() is False

    def test_is_in_venv_inside_venv(self):
        """Should return True when in a virtual environment."""
        from ypkgupgr.venv import is_in_venv

        with patch.object(sys, "prefix", "/fake/venv"):
            with patch.object(sys, "base_prefix", "/usr"):
                assert is_in_venv() is True

    def test_find_venv_in_parents_none_found(self, tmp_path):
        """Should return None when no venv is found in parents."""
        from ypkgupgr.venv import find_venv_in_parents

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = find_venv_in_parents(tmp_path)
            assert result is None

    def test_find_venv_in_parents_finds_venv_unix(self, tmp_path):
        """Should find venv in parent directory on Unix."""
        from ypkgupgr.venv import find_venv_in_parents

        venv_path = tmp_path / "venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        pyvenv_cfg = venv_path / "pyvenv.cfg"
        pyvenv_cfg.write_text("home = /usr\n")

        result = find_venv_in_parents(tmp_path)
        assert result is not None
        assert result.name == "venv"

    def test_find_venv_in_parents_finds_dot_venv(self, tmp_path):
        """Should find .venv in parent directory."""
        from ypkgupgr.venv import find_venv_in_parents

        venv_path = tmp_path / ".venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        pyvenv_cfg = venv_path / "pyvenv.cfg"
        pyvenv_cfg.write_text("home = /usr\n")

        result = find_venv_in_parents(tmp_path)
        assert result is not None
        assert result.name == ".venv"

    def test_find_venv_in_parents_nested_parent(self, tmp_path):
        """Should find venv in a nested parent directory."""
        from ypkgupgr.venv import find_venv_in_parents

        nested = tmp_path / "nested" / "dir"
        nested.mkdir(parents=True)

        venv_path = tmp_path / "venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        pyvenv_cfg = venv_path / "pyvenv.cfg"
        pyvenv_cfg.write_text("home = /usr\n")

        result = find_venv_in_parents(nested)
        assert result is not None
        assert result.name == "venv"

    def test_get_venv_python_with_explicit_path(self, tmp_path):
        """Should return Python path when given explicit venv path."""
        from ypkgupgr.venv import get_venv_python

        venv_path = tmp_path / "venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        result = get_venv_python(str(venv_path))
        assert result is not None
        assert result == python_path

    def test_get_venv_python_with_invalid_path(self):
        """Should return None for invalid venv path."""
        from ypkgupgr.venv import get_venv_python

        result = get_venv_python("/nonexistent/venv")
        assert result is None

    def test_get_venv_python_auto_detect_finds_venv(self, tmp_path):
        """Should auto-detect venv when not specified."""
        from ypkgupgr.venv import get_venv_python

        venv_path = tmp_path / "venv"
        venv_path.mkdir()

        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"

        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.touch()

        pyvenv_cfg = venv_path / "pyvenv.cfg"
        pyvenv_cfg.write_text("home = /usr\n")

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = get_venv_python(None)
            assert result is not None

    def test_venv_names_includes_common_names(self):
        """VENV_NAMES should include common virtual environment names."""
        from ypkgupgr.venv import VENV_NAMES

        assert "venv" in VENV_NAMES
        assert ".venv" in VENV_NAMES
        assert "env" in VENV_NAMES
        assert "virtualenv" in VENV_NAMES
