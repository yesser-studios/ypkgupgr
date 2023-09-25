import subprocess
import sys
import asyncio
import warnings

failed = ""
outdated_count = 0
finished_count = 0
yesserpackageupdater_outdated = False
ran_from_script = False

def progress_ring(complete = False, intermediate = False):
    global outdated_count
    global finished_count

    if sys.platform != "win32":
        return
    
    if outdated_count == 0:
        progress = 0
    else:
        progress = int((finished_count / outdated_count) * 100)
    state = 0

    if complete:
        state = 0
    elif intermediate:
        state = 3
    elif failed == "":
        state = 1
    else:
        state = 2
    
    print(f"{chr(27)}]9;4;{state};{progress}{chr(7)}", end="")
        

async def update(name: str):
    global failed
    global outdated_count
    global finished_count
    global yesserpackageupdater_outdated

    if name == "yesserpackageupdater" and ran_from_script and sys.platform == "win32":
        yesserpackageupdater_outdated = True
        finished_count += 1
        progress_ring()
        print("yesserpackageupdater is outdated. Continuing to update other packages...")

        if failed == "":
            failed = name
        else:
            failed = failed + ", " + name

        return

    # subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", name])
    process = await asyncio.create_subprocess_shell('"' + sys.executable + '"' + " -m pip install --upgrade " + name,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    
    return_code = await process.wait()
    
    finished_count += 1
    progress_ring()

    if return_code == 0:
        print("Successfully updated " + name)
    else:
        print(await process.communicate())
        if failed == "":
            failed = name
        else:
            failed = failed + ", " + name

def update_packages():
    global outdated_count
    global yesserpackageupdater_outdated

    """
        If calling from a python file, please use a subprocess instead.
    """
    
    progress_ring(intermediate = True)

    print("Getting outdated pip packages...")

    # Run pip list command to get the outdated packages
    outdated_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated']).decode('utf-8')

    # Split the output into lines and ignore the header
    lines = outdated_packages.strip().split('\n')[2:]

    if len(lines) <= 0:
        progress_ring(complete = True)
        print("No outdated packages found.")
        return
    
    outdatedCount = len(lines)

    print("Updating packages using pip...")
    # Update each package
    for line in lines:
        package_info = line.split()
        package_name = package_info[0]
        # subprocess.call([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name])
        asyncio.run(update(package_name))

    print()

    if len(failed) == 0:
        print("All outdated packages have been updated. Thank you for using this package.")
    else:
        print("The following packages failed to install: " + failed + "\n")

    if yesserpackageupdater_outdated:
        warnings.warn(f'The yesserpackageupdater package is outdated. Please use "{sys.executable} -m yesserpackageupdater" to update it.\n')
    
    progress_ring(complete = True)

def update_packages_script():
    global ran_from_script

    ran_from_script = True
    update_packages()