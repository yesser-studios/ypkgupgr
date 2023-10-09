import subprocess
import sys
import asyncio

failed = ""
outdated_count = 0
finished_count = 0
yesserpackageupdater_outdated = False
ran_from_script = False

def progress_ring(progress, complete = False, intermediate = False):
    """
        Updates Windows Terminal's progress ring.
    """

    global outdated_count
    global finished_count

    # Checks if the user is on Windows. Otherwise the progress string might be printed and would confuse the user on Linux and Mac.
    if sys.platform != "win32":
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
        

async def update(name: str):
    """
        Updates the package using its name.
    """

    global failed
    global outdated_count
    global finished_count
    global yesserpackageupdater_outdated

    # Checks if the user is on windows and this package is updated using the script. Fixes issue #11 (https://github.com/yesseruser/YesserPackageUpdater/issues/11).
    if name == "yesserpackageupdater" and ran_from_script and sys.platform == "win32":
        yesserpackageupdater_outdated = True
        finished_count += 1
        progress = int((finished_count / outdated_count) * 100)
        progress_ring(progress)
        print("yesserpackageupdater is outdated and you are using the script. Continuing to update other packages... ({progress}% - {finished_count}/{outdated_count} complete or failed)")

        if failed == "":
            failed = name
        else:
            failed += ", " + name

        return

    # Updates the package using python -m pip install --upgrade <name>
    process = await asyncio.create_subprocess_shell('"' + sys.executable + '"' + " -m pip install --upgrade " + name,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    
    # Gets this process' return code.
    return_code = await process.wait()
    
    # Adds a finished and updates the progress ring.
    finished_count += 1
    progress = int((finished_count / outdated_count) * 100)
    progress_ring(progress)

    print() # Empty newline to separate outputs.

    # Checks for update success and if failed, logs the package's name into the failed list.
    if return_code == 0:
        print(f"Successfully updated {name} ({progress}% - {finished_count}/{outdated_count} complete or failed)")
    else:
        # Separates the output string by lines.
        (out, err) = await process.communicate()
        for line in out.strip().decode().splitlines():
            print(line)
        
        print(f"{name} failed to update. ({progress}% - {finished_count}/{outdated_count} complete or failed)")
        
        if failed == "":
            failed = name
        else:
            failed += ", " + name

def update_packages():
    """
        If calling from a python file, please use a subprocess instead.
    """

    global outdated_count
    global yesserpackageupdater_outdated
    
    progress_ring(progress = 0, intermediate = True)

    print("Getting outdated pip packages...")

    # Runs the pip list --outdated command to get the outdated packages.
    outdated_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated']).decode('utf-8')

    # Splits the output into lines and ignore the header.
    lines = outdated_packages.strip().split('\n')[2:]

    # Checks if there are any outdated packages.
    if len(lines) <= 0:
        progress_ring(progress = 100, complete = True)
        print("No outdated packages found.")
        return
    
    outdated_count = len(lines)

    print("Updating packages using pip...")

    # Updates each package
    for line in lines:
        package_info = line.split()
        package_name = package_info[0]
        asyncio.run(update(package_name))

    # Empty line before conclusion.
    print()

    # Prints conclusion.
    if len(failed) == 0:
        print("All outdated packages have been updated. Thank you for using this package.")
    else:
        print("The following packages failed to install: " + failed + "\n")

    # Warns the user if yesserpackageupdater hasn't been updated.
    if yesserpackageupdater_outdated:
        print(f'The yesserpackageupdater package is outdated, and you are using the script. Please use "{sys.executable} -m yesserpackageupdater" to update it.\n')
    
    progress_ring(progress = 100,complete = True)

def update_packages_script():
    """
        Runs update_packages() and sets ran_from_script to True. Contributes to fixing issue #11. (https://github.com/yesseruser/YesserPackageUpdater/issues/11)
    """

    global ran_from_script

    ran_from_script = True
    update_packages()