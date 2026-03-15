import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_sys_modules():
    """Mock sys module attributes for venv tests."""
    with patch.object(sys, "prefix", sys.base_prefix):
        with patch.object(sys, "base_prefix", sys.base_prefix):
            with patch.object(sys, "executable", "/usr/bin/python3"):
                yield


@pytest.fixture
def tmp_venv(tmp_path):
    """Create a temporary virtual environment structure."""
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

    return venv_path


@pytest.fixture
def tmp_ignored_file(tmp_path, monkeypatch):
    """Create a temporary ignored file."""
    ignored_file = tmp_path / "ignored.cfg"
    monkeypatch.setattr("ypkgupgr.appdata.ignored_path", str(ignored_file))
    return ignored_file


@pytest.fixture
def mock_platformdirs(tmp_path, monkeypatch):
    """Mock platformdirs to use temporary directories."""

    def mock_user_data_dir(appname, author=None):
        return str(tmp_path / "data")

    def mock_user_log_dir(appname, author=None):
        return str(tmp_path / "logs")

    monkeypatch.setattr("platformdirs.user_data_dir", mock_user_data_dir)
    monkeypatch.setattr("platformdirs.user_log_dir", mock_user_log_dir)


@pytest.fixture
def reset_ignored_list():
    """Reset the global ignored list before and after tests."""
    import ypkgupgr.ignored as ignored_module

    ignored_module.ignored = []
    yield
    ignored_module.ignored = []


@pytest.fixture
def reset_misc_globals():
    """Reset global variables in misc module."""
    import ypkgupgr.misc as misc_module

    misc_module.failed = ""
    misc_module.outdated_count = 0
    misc_module.finished_count = 0
    misc_module.ypkgupgr_outdated = False
    misc_module.ran_from_script = False
    misc_module.line_count = 0
    yield
    misc_module.failed = ""
    misc_module.outdated_count = 0
    misc_module.finished_count = 0
    misc_module.ypkgupgr_outdated = False
    misc_module.ran_from_script = False
    misc_module.line_count = 0
