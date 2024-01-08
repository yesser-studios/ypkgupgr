import subprocess
import sys
import os
import asyncio
import logging

from logging import FileHandler
import platformdirs

class Colors:
    WHITE: str = '\u001b[37m'
    RED: str = '\u001b[31m'
    YELLOW: str = '\u001b[33m'
    GREEN: str = '\u001b[32m'
    RESET: str = '\033[0m'

failed = ""
outdated_count = 0
finished_count = 0
ypkgupgr_outdated = False
ran_from_script = False
logger = logging.getLogger("logger")

line_length = dict()
line_count = 0

app_name = "ypkgupgr"
author_name = "Yesser Studios"

appdata_dir = platformdirs.user_data_dir(app_name, author_name)
ignored_path = appdata_dir + "/ignored.cfg"
log_dir = platformdirs.user_log_dir(app_name, author_name)
log_file = log_dir + "/log.log"

# Log file location:
# Windows: %LOCALAPPDATA%\Yesser Studios\ypkgupgr\Logs\log.log
# MacOS: ~/Library/Logs/ypkgupgr
# Linux: ~/.local/state/ypkgupgr/log

ignored = []

def create_appdata_dirs():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir) # Create the logs directory. Will also create the AppData directory.

def ignore_packages(packages: list):
    logger.info("Ignoring packages:")
    logger.info(list)

    with open(ignored_path, "a") as file:
        file.write("\n".join(packages) + "\n")
        file.flush()
        file.close()
    
    logger.info("Ignored packages.")
    print("Package/s ignored.")

def unignore_packages(packages: list):
    logger.info("Unignoring packages:")
    logger.info(list)

    lines = None

    with open(ignored_path, "r") as file:
        lines = file.readlines()
        file.close()

    for package in packages:
        with open(ignored_path, "w") as file: # Open in overwrite mode
            for line in lines:
                if line.strip() != package: # Check if the line is identical with package
                    file.write(line + "\n") # If not, write it to overwrite
            file.flush()
            file.close()
    
    logger.info("Packages unignored.")
    print("Package/s unignored.")

def unignore_all():
    with open(ignored_path, "w") as file:
        file.truncate(0)
        file.flush()
        file.close()

def get_ignored_packages():
    logger.info("Getting ignored packages...")

    if (not os.path.exists(ignored_path)):
        logger.info("Ignored file not found. Continuing without ignoring packages...")
        return

    with open(ignored_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            ignored.append(line.strip())


def clear_screen():
    print("\033c", end='')

def init_logging():
    """
        Initialises the logger.
    """

    global logger

    logger.setLevel(logging.DEBUG if "--log-debug" in sys.argv else logging.INFO)
    file_handler = FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%d. %m. %Y %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if "--clear-log" in sys.argv:
        with open(log_file, 'w'):
            pass

    logger.info("Logger initialized.")

def help():
    global logger
    
    logger.debug("Showing help...")

    print("To update all packages, run the module without any parameters.")
    print("-? | --help: Displays this help without updating packages.")
    print("--clear-log: Clears the log file before writing to it.")
    print("--log-debug: Logs debug information to the log file.")
    print("--ignore: Saves all packages placed after this to ignore. Does not update packages.")
    print("--unignore: Unignores all packages placed after this. Does not update packages.")
    print("--unignore-all: Unignores all ignored packages. Does not update packages.")

    logger.debug("Help shown.")

def progress_ring(progress, complete = False, intermediate = False):
    """
        Updates Windows Terminal's progress ring.
    """

    global outdated_count
    global finished_count

    # Checks if the user is on Windows. Otherwise the progress string might be printed and would confuse the user on Linux and Mac.
    if sys.platform != "win32":
        logger.debug("Progress ring not shown because platform is not Windows.")
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

    logger.debug(f"Progress ring updated with the following data: State: {state}; Progress: {progress}")
        

def progress_update(line: int, text: str):
    for i in range(line_length[line] + 1):
        text += " "
    print(f"\033[{line};1H" + Colors.RESET + text)
    line_length[line] = len(text)

async def update(name: str, line: int):
    """
        Updates the package using its name.
    """

    global failed
    global outdated_count
    global finished_count
    global ypkgupgr_outdated

    get_ignored_packages()
    
    if (name in ignored): # Package in ignored
        logger.info(f"Package {name} ignored.")
        progress_update(line, f"{name}: {Colors.YELLOW}Ignored")
        finished_count += 1
        progress = int((finished_count / outdated_count) * 100)
        progress_ring(progress)
        return

    logger.info(f"Updating {name}")
    progress_update(line, f"{name}: {Colors.WHITE}Updating...")

    # Checks if the user is on windows and this package is updated using the script. Fixes issue #11 (https://github.com/yesseruser/ypkgupgr/issues/11).
    if name == "ypkgupgr" and ran_from_script and sys.platform == "win32":
        ypkgupgr_outdated = True
        finished_count += 1
        progress = int((finished_count / outdated_count) * 100)
        progress_ring(progress)
        progress_update(line, f"{name}: {Colors.YELLOW}Skipped")
        # print(f"ypkgupgr is outdated and you are using the script. Continuing to update other packages... ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        logger.info(f"Skipping ypkgupgr. See bottom of the logs for details.")

        if failed == "":
            failed = name
        else:
            failed += ", " + name

        logger.debug("Added ypkgupgr into failed.")

        return

    # Updates the package using python -m pip install --upgrade <name>
    process = await asyncio.create_subprocess_shell('"' + sys.executable + '"' + " -m pip install --upgrade " + name,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    
    logger.debug("Subprocess shell created.")
    
    # Gets this process' return code.
    return_code = await process.wait()

    logger.debug(f"Subprocess ended with code {return_code}")
    
    # Adds a finished and updates the progress ring.
    finished_count += 1
    progress = int((finished_count / outdated_count) * 100)
    progress_ring(progress)

    # Checks for update success and if failed, logs the package's name into the failed list.
    if return_code == 0:
        progress_update(line, f"{name}: {Colors.GREEN}Done")
        # print(f"Successfully updated {name} ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        logger.info(f"Successfully updated {name}.")
    else:
        logger.error(f"{name} failed to update; below is pip output:")

        # Separates the output string by lines.
        (out, err) = await process.communicate()
        for errline in out.strip().decode().splitlines():
            logger.error(errline)

        logger.info("End of pip output.")
        
        progress_update(line, f"{name}: {Colors.RED}Error")
        # print(f"{name} failed to update. ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        
        if failed == "":
            failed = name
        else:
            failed += ", " + name

        logger.debug(f"Added {name} to failed.")

async def start_updates(lines: list[str]):
    """Updates each package."""
    global line_count

    tasks = []

    line_no = 3 # Tasks start at line 3, because there was 1 line already printed + one to separate.
    for line in lines:
        package_info = line.split()
        package_name = package_info[0]

        line_length[line_no] = 0

        logger.debug(f"Starting to update {package_name}")
        tasks.append(asyncio.create_task(update(package_name, line_no)))

        line_no += 1
    
    line_count = line_no
    
    for task in tasks:
        await task

def update_packages():
    """
        If calling from a python file, please use a subprocess instead.
    """

    global outdated_count
    global ypkgupgr_outdated

    # Log commands are handled in init_logging.

    if ("-?" in sys.argv or "--help" in sys.argv):
        help()
        return
    
    if ("--ignore" in sys.argv):
        ignore_packages(sys.argv[sys.argv.index("--ignore") + 1:])
        # ^ ignores everything after --ignore.
        return
    
    if ("--unignore" in sys.argv):
        unignore_packages(sys.argv[sys.argv.index("--unignore") + 1:])
        # ^ unignores everything after --unignore.
        return
    
    if ("--unignore-all" in sys.argv):
        unignore_all()
        return

    logger.info(f"Starting update. Platform: {sys.platform}")
    
    # Clears the screen.
    clear_screen()

    progress_ring(progress = 0, intermediate = True)


    print("Getting outdated pip packages...")
    logger.info("Getting outdated packages.")

    # Runs the pip list --outdated command to get the outdated packages.
    outdated_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated', '--disable-pip-version-check']).decode('utf-8')

    # Splits the output into lines and ignore the header.
    lines = outdated_packages.strip().split('\n')[2:]

    # Checks if there are any outdated packages.
    if len(lines) <= 0:
        progress_ring(progress = 100, complete = True)
        print("No outdated packages found.")
        logger.info("No outdated packages.")
        return
    
    outdated_count = len(lines)

    logger.info(f"Outdated packages: {lines}")

    clear_screen()

    print("Updating packages using pip...")

    logger.info("Starting to update packages...")

    asyncio.run(start_updates(lines))

    logger.info("Finished updating packages.")

    # Empty line before conclusion.
    print(f"\033[{line_count};1H" + Colors.RESET)

    # Prints conclusion.
    if len(failed) == 0:
        print("All outdated packages have been updated. Thank you for using this package.")
        logger.info(f"All outdated packages updated with a total of {outdated_count} packages.")
    else:
        print("The following packages failed to install: " + failed + "\n")
        logger.info(f"The following packages failed to install: {failed}")

    # Warns the user if ypkgupgr hasn't been updated.
    if ypkgupgr_outdated:
        print(f'The ypkgupgr package is outdated, and you are using the script. Please use "{sys.executable} -m ypkgupgr" to update it.\n')
        logger.info("ypkgupgr is outdated and the script is used on Windows.")
    
    progress_ring(progress = 100,complete = True)

def update_packages_script():
    """
        Runs update_packages() and sets ran_from_script to True. Contributes to fixing issue #11. (https://github.com/yesseruser/ypkgupgr/issues/11)
    """

    global ran_from_script

    ran_from_script = True

    create_appdata_dirs()

    init_logging()

    logger.info("Starting from script...")

    update_packages()
