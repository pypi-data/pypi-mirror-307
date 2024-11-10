from .mtax_cache import MtaxCache
from .cache_app import (
    cache_,
    add_ as add_to_cache,
    incr_ as incr_in_cache,
    set_ as set_item_to_cache,
    get_ as get_item_from_cache,
    decr_ as decr_in_cache,
    clear_ as clear_cache,
    reset_ as reset_cache,
    remove_ as remove_item_from_cache,
    list_ as list_items_in_cache,
    info_ as show_info_of_cache)


__version__ = 'v1.0.0'


__all__ = [
    "MtaxCache",
    "cache_",
    "add_to_cache",
    "incr_in_cache",
    "set_item_to_cache",
    "get_item_from_cache",
    "decr_in_cache",
    "clear_cache",
    "remove_item_from_cache",
    "reset_cache",
    "list_items_in_cache",
    "show_info_of_cache",
    "__version__"]
