import subprocess
import sys
import os
import asyncio
import logging
import platformdirs
import click
from .colors import Colors
from .consts import APP_NAME, AUTHOR_NAME
from .logs import *
from .appdata import create_appdata_dirs
from .ignored import ignored, get_ignored_packages, ignore_packages, unignore_packages, unignore_all
from .graphics import progress_update, progress_ring, clear_screen
from .misc import *

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

@click.command()
@click.option('--clear-log', is_flag=True, help='Clear the log file before writing to it.')
@click.option('--log-debug', is_flag=True, help='Log debug information.')
@click.option('--ignore', help='Add the package to the ignored file and exit.', multiple=True)
@click.option('--unignore', help='Remove the package from the ignored file (if present) and exit.', multiple=True)
@click.option('--unignore-all', is_flag=True, help='Clear the ignored file and exit.')
def update_command(clear_log, log_debug, ignore, unignore, unignore_all):
    print(clear_log, log_debug, ignore, unignore, unignore_all)

def run_from_script():
    """
        Runs update_packages() and sets ran_from_script to True. That contributes to fixing issue #11 of the original repo. (https://github.com/yesseruser/yesserpackageupdater/issues/11)
    """

    global ran_from_script

    ran_from_script = True

    create_appdata_dirs()

    init_logging()

    logger.info("Starting from script...")

    # update_packages()

    update_command()