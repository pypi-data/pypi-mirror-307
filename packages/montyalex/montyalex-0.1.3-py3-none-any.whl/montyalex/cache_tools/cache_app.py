from functools import cache

from montyalex.typer_tools import Option, Typer
from .mtax_cache import MtaxCache
from .timecache_app import time_


cache_: Typer = Typer(
    name='cache',
    add_help_option=False)
cache_.add_typer(time_)

@cache_.command(name='add', add_help_option=False)
def add_(
    *,
    key: str,
    value: str,
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console'),
    timezone: str = 'Etc/Greenwich'):
    """Add a key-value pair in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.add_item((key, value), silent)

@cache
@cache_.command(name='incr', add_help_option=False)
def incr_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Increment an item count in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    return mtax.incr_item(key, silent)

@cache_.command(name='set', add_help_option=False)
def set_(
    *,
    key: str,
    value: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Sets a key-value pair in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.set_item((key, value), silent)

@cache
@cache_.command(name='get', add_help_option=False)
def get_(
    *,
    key: str,
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Gets a key-value pair from the cache if the key exists"""
    mtax: MtaxCache = MtaxCache()
    return mtax.get_item(key, silent)

@cache
@cache_.command(name='decr', add_help_option=False)
def decr_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Decrement an item count in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    return mtax.decr_item(key, silent)

@cache_.command(name='clear', add_help_option=False)
def clear_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Clear all the key-value pairs in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.clear(silent)

@cache_.command(name='reset', add_help_option=False)
def reset_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Reset stuck key-value pairs in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.reset(silent)

@cache_.command(name='remove', add_help_option=False)
def remove_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Remove the matching key from the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.remove(key, silent)

@cache_.command(name='list', add_help_option=False)
def list_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """List the key-value pairs stored in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.list_k_v_pairs(silent)

@cache_.command(name='info', add_help_option=False)
def info_(
    *,
    timezone: str = 'Etc/Greenwich',
    list_items: bool = Option(
        False, '-list', help='List the key-value pairs stored in the cache (list command)'),
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Shows various info and current size of caches"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.info(list_items, silent)
