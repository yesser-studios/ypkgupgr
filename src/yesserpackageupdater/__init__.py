import subprocess
import sys
import os
import asyncio
import logging
from logging import FileHandler

failed = ""
outdated_count = 0
finished_count = 0
yesserpackageupdater_outdated = False
ran_from_script = False
logger = logging.getLogger("logger")
log_file = f"{os.path.dirname(os.path.realpath(__file__))}/logs.log"

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
        

async def update(name: str):
    """
        Updates the package using its name.
    """

    global failed
    global outdated_count
    global finished_count
    global yesserpackageupdater_outdated

    logger.info(f"Updating {name}")

    # Checks if the user is on windows and this package is updated using the script. Fixes issue #11 (https://github.com/yesseruser/YesserPackageUpdater/issues/11).
    if name == "yesserpackageupdater" and ran_from_script and sys.platform == "win32":
        yesserpackageupdater_outdated = True
        finished_count += 1
        progress = int((finished_count / outdated_count) * 100)
        progress_ring(progress)
        print(f"yesserpackageupdater is outdated and you are using the script. Continuing to update other packages... ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        logger.info(f"Skipping yesserpackageupdater. See bottom of the logs for details.")

        if failed == "":
            failed = name
        else:
            failed += ", " + name

        logger.debug("Added yesserpackageupdater into failed.")

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

    print() # Empty newline to separate outputs.

    # Checks for update success and if failed, logs the package's name into the failed list.
    if return_code == 0:
        print(f"Successfully updated {name} ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        logger.info(f"Successfully updated {name}.")
    else:
        logger.error(f"{name} failed to update; below is pip output:")

        # Separates the output string by lines.
        (out, err) = await process.communicate()
        for line in out.strip().decode().splitlines():
            print(line)
            logger.error(line)

        logger.info("End of pip output.")
        
        print(f"{name} failed to update. ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        
        if failed == "":
            failed = name
        else:
            failed += ", " + name

        logger.debug(f"Added {name} to failed.")

def update_packages():
    """
        If calling from a python file, please use a subprocess instead.
    """

    global outdated_count
    global yesserpackageupdater_outdated

    logger.info(f"Starting update. Platform: {sys.platform}")
    
    progress_ring(progress = 0, intermediate = True)

    print("Getting outdated pip packages...")
    logger.info("Getting outdated packages.")

    # Runs the pip list --outdated command to get the outdated packages.
    outdated_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated']).decode('utf-8')

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

    print("Updating packages using pip...")

    logger.info("Starting to update packages...")

    # Updates each package
    for line in lines:
        package_info = line.split()
        package_name = package_info[0]
        logger.debug(f"Starting to update {package_name}")
        asyncio.run(update(package_name))

    logger.info("Finished updating packages.")

    # Empty line before conclusion.
    print()

    # Prints conclusion.
    if len(failed) == 0:
        print("All outdated packages have been updated. Thank you for using this package.")
        logger.info(f"All outdated packages updated with a total of {outdated_count} packages.")
    else:
        print("The following packages failed to install: " + failed + "\n")
        logger.info(f"The following packages failed to install: {failed}")

    # Warns the user if yesserpackageupdater hasn't been updated.
    if yesserpackageupdater_outdated:
        print(f'The yesserpackageupdater package is outdated, and you are using the script. Please use "{sys.executable} -m yesserpackageupdater" to update it.\n')
        logger.info("yesserpackageupdater is outdated and the script is used on Windows.")
    
    progress_ring(progress = 100,complete = True)

def update_packages_script():
    """
        Runs update_packages() and sets ran_from_script to True. Contributes to fixing issue #11. (https://github.com/yesseruser/YesserPackageUpdater/issues/11)
    """

    global ran_from_script

    ran_from_script = True
    init_logging()

    logger.info("Starting from script...")

    update_packages()