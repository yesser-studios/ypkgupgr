from .colors import Colors

failed: str = ""
outdated_count: int = 0
finished_count: int = 0

ypkgupgr_outdated: bool = False

ran_from_script: bool = False

line_count: int = 0
current_lines: list[str] = [
    Colors.RESET + "Getting outdated pip packages...",
    Colors.RESET + "Updating packages using pip...",
]
