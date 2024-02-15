from .colors import Colors

failed = ""
outdated_count = 0
finished_count = 0

ypkgupgr_outdated = False

ran_from_script = False

line_count = 0
current_lines = [Colors.RESET + "Getting outdated pip packages...", Colors.RESET + "Updating packages using pip..."]
