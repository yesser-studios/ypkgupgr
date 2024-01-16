from . import update_packages, init_logging
from .appdata import create_appdata_dirs

create_appdata_dirs()
init_logging()
update_packages()