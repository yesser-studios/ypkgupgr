import subprocess
import sys
import asyncio

failed = ""

async def update(name: str):
    global failed

    # subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", name])
    process = await asyncio.create_subprocess_shell('"' + sys.executable + " -m pip install --upgrade " + name + '"',
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    
    return_code = await process.wait()
    if return_code == 0:
        print("Successfully updated " + name)
    else:
        print(await process.communicate())
        if len(failed) == 0:
            failed = name
        else:
            failed = failed + ", " + name

def update_packages():
    """
        If calling from a python file, please use a subprocess instead.
    """
    
    print("Getting outdated pip packages...")
    # Run pip list command to get the outdated packages
    outdated_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated']).decode('utf-8')

    # Split the output into lines and ignore the header
    lines = outdated_packages.strip().split('\n')[2:]

    if len(lines) <= 0:
        print("No outdated packages found.")
        return

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
        print("The following packages failed to install: " + failed)