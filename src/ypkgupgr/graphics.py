import os
import io

from .logs import log_debug
from .colors import Colors
from .misc import failed, current_lines


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def progress_ring(progress, complete=False, intermediate=False):
    """
        Updates Windows Terminal's progress ring.
    """

    # Checks if the WT_SESSION variable is set to prevent printing on consoles where this isn't supported.
    if "WT_SESSION" not in os.environ:
        log_debug("Progress ring not shown because WT_SESSION key not present.")
        return

    # Gets the correct progress ring state.
    state = 0
    if complete:
        state = 0
    elif intermediate:
        state = 3
    elif failed == "":
        state = 1
    else:
        state = 2

    # Show progress https://github.com/MicrosoftDocs/terminal/blob/main/TerminalDocs/tutorials/progress-bar-sequences.md
    print(f"{chr(27)}]9;4;{state};{progress}{chr(7)}", end="")

    log_debug(f"Progress ring updated with the following data: State: {state}; Progress: {progress}")


def progress_update(line: int, text: str):
    if line < len(current_lines):
        current_lines[line] = Colors.RESET + text
    elif line == len(current_lines):
        current_lines.append(Colors.RESET + text)
    else:
        for i in range(0, line - (len(current_lines))):
            current_lines.append("")
        current_lines.append(Colors.RESET + text)

    buffer = io.StringIO()  # To show processed output all at once
    for string in current_lines:
        buffer.write(string + "\n")
    buffer.flush()

    clear_screen()
    print(buffer.getvalue())
