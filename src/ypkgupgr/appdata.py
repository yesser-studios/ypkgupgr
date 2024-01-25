import os
import platformdirs
from .consts import APP_NAME, AUTHOR_NAME

appdata_dir = platformdirs.user_data_dir(APP_NAME, AUTHOR_NAME)
ignored_path = appdata_dir + "/ignored.cfg"
log_dir = platformdirs.user_log_dir(APP_NAME, AUTHOR_NAME)
log_file = log_dir + "/log.log"

def create_appdata_dirs():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir) # Create the logs directory. Will also create the AppData directory.