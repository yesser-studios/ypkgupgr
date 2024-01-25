import os
from .logs import log_info
from .appdata import ignored_path

ignored = []

def ignore_packages(packages: list):
    log_info("Ignoring packages:")
    log_info(packages)

    with open(ignored_path, "a") as file:
        file.write("\n".join(packages) + "\n")
        file.flush()
        file.close()
    
    log_info("Ignored packages.")
    print("Package/s ignored.")

def unignore_packages(packages: list):
    log_info("Unignoring packages:")
    log_info(packages)

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
    
    log_info("Packages unignored.")
    print("Package/s unignored.")

def unignore_all():
    with open(ignored_path, "w") as file:
        file.truncate(0)
        file.flush()
        file.close()
    
    log_info("All packages unignored.")
    print("All packages unignored.")

def get_ignored_packages():
    log_info("Getting ignored packages...")

    if (not os.path.exists(ignored_path)):
        log_info("Ignored file not found. Continuing without ignoring packages...")
        return

    with open(ignored_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            ignored.append(line.strip())