import sys
from .logs import log_debug
from .colors import Colors
from .misc import failed, line_length

def clear_screen():
    print("\033c", end='')

def progress_ring(progress, complete = False, intermediate = False):
    """
        Updates Windows Terminal's progress ring.
    """

    global outdated_count
    global finished_count

    # Checks if the user is on Windows. Otherwise the progress string might be printed and would confuse the user on Linux and Mac.
    if sys.platform != "win32":
        log_debug("Progress ring not shown because platform is not Windows.")
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
    
    # Prints the progress string according to https://github.com/MicrosoftDocs/terminal/blob/main/TerminalDocs/tutorials/progress-bar-sequences.md
    print(f"{chr(27)}]9;4;{state};{progress}{chr(7)}", end="")

    log_debug(f"Progress ring updated with the following data: State: {state}; Progress: {progress}")

def progress_update(line: int, text: str):
    for i in range(line_length[line] + 1):
        text += " "
    print(f"\033[{line};1H" + Colors.RESET + text)
    line_length[line] = len(text)