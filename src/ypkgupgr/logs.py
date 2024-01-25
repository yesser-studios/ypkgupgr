from .appdata import log_dir, log_file
import logging

logger = logging.getLogger("logger")

# Log file location:
# Windows: %LOCALAPPDATA%\Yesser Studios\ypkgupgr\Logs\log.log
# MacOS: ~/Library/Logs/ypkgupgr
# Linux: ~/.local/state/ypkgupgr/log

def init_logging(clear_log, log_debug):
    """
        Initialises the logger.
    """

    global logger

    logger.setLevel(logging.DEBUG if log_debug else logging.INFO)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%d. %m. %Y %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(file_handler)

    if clear_log:
        with open(log_file, 'w'):
            pass
        logger.debug("Debug logging mode on.")
    logger.info("Logger initialized.")

def log_info(log: str):
    logger.info(log)

def log_debug(log: str):
    logger.debug(log)