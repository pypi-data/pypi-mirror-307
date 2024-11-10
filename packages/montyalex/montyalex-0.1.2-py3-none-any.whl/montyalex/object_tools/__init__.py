from .enumeration import Key, Value
from .exceptions import MontyKeyValueError, MontyJSONError, MontyRangeError
from .pickling import pdumps, ploads
from .singleton import singleton_decorator as singleton


__version__ = 'v1.0.0'


__all__ = [
    "Key",
    "Value",
    "MontyKeyValueError",
    "MontyJSONError",
    "MontyRangeError",
    "pdumps",
    "ploads",
    "singleton",
    "__version__"]
