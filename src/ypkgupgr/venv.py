import sys
from pathlib import Path
from typing import Optional

VENV_NAMES = ("venv", ".venv", "env", "virtualenv")


def is_in_venv() -> bool:
    """Check if currently running inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def find_venv_in_parents(start_path: Optional[Path] = None) -> Optional[Path]:
    """Look for a virtual environment in the current directory or parent directories."""
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path).resolve()

    current = start_path

    while True:
        for name in VENV_NAMES:
            venv_path = current / name
            if venv_path.is_dir():
                python_path = venv_path / "bin" / "python"
                if (
                    python_path.exists()
                    or (venv_path / "Scripts" / "python.exe").exists()
                ):
                    return venv_path

        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def get_venv_python(venv_path: Optional[str] = None) -> Optional[Path]:
    """Get the Python executable path for the detected or specified venv."""
    target_venv: Optional[Path] = None

    if venv_path:
        target_venv = Path(venv_path).resolve()
    else:
        found_venv = find_venv_in_parents()
        if found_venv:
            target_venv = found_venv
        elif is_in_venv():
            return Path(sys.executable)
        else:
            return None

    if target_venv is None:
        return None

    if sys.platform == "win32":
        python_exe = target_venv / "Scripts" / "python.exe"
    else:
        python_exe = target_venv / "bin" / "python"

    if python_exe.exists():
        return python_exe

    return None
