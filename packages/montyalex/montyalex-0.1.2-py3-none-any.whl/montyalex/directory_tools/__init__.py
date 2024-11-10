from .datedirs import create_date_directories as datedirs, remove_date_directories as rmdatedirs
from .simpledirs import (
    create_simple_directories as simpledirs,
    remove_simple_directories as rmsimpledirs)


__version__ = 'v1.0.0'


__all__ = [
    "datedirs",
    "rmdatedirs",
    "simpledirs",
    "rmsimpledirs",
    "__version__"]
