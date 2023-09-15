import subprocess
import sys

def update_packages():
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
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name])

    print("All outdated packages have been updated. Thank you for using this package.")