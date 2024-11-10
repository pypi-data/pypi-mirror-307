from montyalex.time_tools import MtaxTime
from montyalex.typer_tools import Option, Typer
from .mtax_cache import MtaxCache
from .zonecache_app import zone_


time_: Typer = Typer(
    name='time',
    help='Manage time-data in the cache')
time_.add_typer(zone_)

@time_.command(name='reset')
def reset_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Reset timestamp in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.remove('_timestamp_', silent)
    set_(timezone=timezone, silent=silent)

@time_.command(name='set')
def set_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Set timestamp in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.set_item(('_timestamp_', MtaxTime(timezone).timestamp()), silent)

@time_.command(name='get')
def get_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Set timestamp in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.get_item('_timestamp_', silent)
