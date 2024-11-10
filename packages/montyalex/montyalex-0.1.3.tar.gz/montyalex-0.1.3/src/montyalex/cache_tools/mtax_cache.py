import platform
from diskcache import Cache
import psutil

from montyalex.console_tools import richconsole, success_stm
from montyalex.fs_tools import current_working_dir, joinpaths, pathexists
from montyalex.time_tools import MtaxTime
from montyalex.typing_tools import NoneType
from .cache_helpers import remove_cache__dir

print = richconsole.print


DIR = joinpaths('.mtax', 'cache')
mtax: Cache = Cache(DIR)
os_name = platform.system()
os_strength = platform.processor()
py_ver = platform.python_version()
cache_exists = joinpaths(current_working_dir, DIR, 'cache.db')

svmem = psutil.virtual_memory()

total_ram_bytes = svmem.total
total_ram_gb = total_ram_bytes / (1024 ** 3)

available_ram_bytes = svmem.available
available_ram_gb = available_ram_bytes / (1024 ** 3)

used_ram_bytes = total_ram_bytes - available_ram_bytes
used_ram_gb = used_ram_bytes / (1024 ** 3)

class MtaxCache:
    def __init__(self, timezone: str = 'Etc/Greenwich') -> None:
        self.cache = mtax
        self.status: str = 'Ok'
        self.os_ = os_name
        self.os_strength = os_strength
        self.py_ver = py_ver
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = available_ram_gb
        self.used_ram_gb = used_ram_gb
        self.datetime: MtaxTime = MtaxTime(timezone)

    def add_item(self, item: tuple[str, str], silent: bool = False):
        if not silent:
            print(f'Adding {item[0]!r} to Cache')
        self.cache.add('_timestamp_', self.datetime.timestamp())
        self.cache.add(item[0], item[1])
        if not silent:
            print(f'{success_stm}, Added {item[0]!r} to Cache')

    def set_item(self, item: tuple[str, str], silent: bool = False):
        if not silent:
            print(f'Setting {item[0]!r} to {item[1]!r} in the Cache')
        self.cache.set('_timestamp_', self.datetime.timestamp())
        self.cache.set(item[0], item[1])
        print(f'{success_stm}, Set {item[0]!r} to {item[1]!r} in the Cache')

    def get_item(self, key_: str, silent: bool = False):
        if not silent:
            print(f'Getting {key_!r} from the Cache')
        item_value = self.cache.get(key_)
        if not silent:
            print(f'{success_stm}, Got {key_!r} from the Cache')
            print(f'The value for {key_!r} in the Cache is {item_value!r}')
        if not silent:
            print(f'{key_!r}={item_value!r}')
        return item_value

    def incr_item(self, key_: str, silent: bool = False):
        if not silent:
            print(f'Incrementing {key_!r} in the Cache')
        item_value = self.cache.incr(key_)
        item_value = max(item_value, 0)
        if not silent:
            print(f'{success_stm}, Incremented {key_!r} in the Cache to {item_value}')
        return item_value

    def decr_item(self, key_: str, silent: bool = False):
        if not silent:
            print(f'Decrementing {key_!r} in the Cache')
        item_value = self.cache.decr(key_)
        item_value = max(item_value, 0)
        if not silent:
            print(f'{success_stm}, Decremented {key_!r} in the Cache to {item_value}')
        return item_value

    def clear(self, silent: bool = False):
        if not silent:
            print('Clearing Cache')
        self.cache.clear()
        remove_cache__dir(DIR, silent)
        if not silent:
            print('Cache Cleared')

    def reset(self, silent: bool = False):
        if not silent:
            print('Resetting Cache')
        self.remove('_python_', silent)
        self.remove('_datedirs_', silent)
        self.remove('_cache-tools_', silent)
        self.remove('_directory-tools_', silent)
        self.add_item(('_python_', f'v{platform.python_version()}'), silent)
        self.add_item(('_datedirs_', 'v1.0.0'), silent)
        self.add_item(('_cache-tools_', 'v1.0.0'), silent)
        self.add_item(('_directory-tools_', 'v1.0.0'), silent)
        if not silent:
            print('Cache Reset')

    def remove(self, key_: str, silent: bool = False):
        if not silent:
            print(f'Removing {key_!r}')
        self.cache.delete(key_)
        if not silent:
            print(f'{success_stm}, Removed {key_!r} from Cache')

    def list_k_v_pairs(self, silent: bool = False):
        cached_items = list(self.cache)
        cached_items.sort()
        for key in cached_items:
            value = self.cache.get(key)
            print(f'[bold]{key}[/]: {value!r}')
        if not silent:
            ...

    def info(self, list_: bool = False, silent: bool = False):
        print("[bold]Info[/]: [")
        print(f"  [bold]Current[/]: {self.datetime.timestamp()!r}")
        if self.status == 'Ok':
            print(f"  [bold]Status[/]: [green]{self.status!r}[/]")
        else:
            print(f"  [bold]Status[/]: [red]{self.status!r}[/]")
        print(f"  [bold]System Processor[/]: {self.os_strength!r}")
        print(f"  [bold]Operating System[/]: {self.os_!r}")
        if self.os_strength and self.os_:
            print(f"    [bold]Python Version[/]: [yellow]'v{self.py_ver}'[/]")
            if self.available_ram_gb:
                print(f"    [bold]RAM Available[/]: [sky_blue2]{self.available_ram_gb:.2f}GB[/]")
            else:
                print(f"    [bold]RAM Available[/]: [orange4]{0:.2f}GB [bold]???[/][/] NONE FOUND")
            if self.used_ram_gb:
                print(f"    [bold]RAM Used[/]: [deep_pink3]{self.used_ram_gb:.2f}GB[/]")
            else:
                print(f"    [bold]RAM Used[/]: [green1]{0:.2f}GB [bold]???[/][/] NONE FOUND")
            if self.total_ram_gb > 0:
                print(f"    [bold]RAM Total[/]: [sky_blue2]{self.total_ram_gb:.2f}GB[/]")
            else:
                print(f"    [bold]RAM Total[/]: [orange4]{0:.2f}GB [bold]???[/][/] NONE FOUND")
            print("    [bold]Status[/]: [green]'Good'[/]")
        else:
            print("    [bold]Status[/]: [red]'Bad'[/]")
        if pathexists(cache_exists):
            print(f'  [bold]Cache Directory[/]: [green]{DIR!r}[/]')
            print("    [bold]File[/]: [green]'cache.db'[/]")
        else:
            print(f'  [bold]Cache Directory[/]: [red]{DIR!r}[/]')
            print("    [bold]File[/]: [red]'cache.db'[/] [dim](does not exist)[/]")
        py_ver_cached = self.get_item('_python_', True)
        cat_ver_cached = self.get_item('_cache-tools_', True)
        cot_ver_cached = self.get_item('_console-tools_', True)
        dir_ver_cached = self.get_item('_directory-tools_', True)
        if isinstance(py_ver_cached, NoneType):
            print(f"    [bold]Python Version[/]: {py_ver_cached!r}")
        else:
            print(f"    [bold]Python Version[/]: [yellow]{py_ver_cached!r}[/]")
        if isinstance(cat_ver_cached, NoneType):
            print(f"    [bold]CacheTools Version[/]: {cat_ver_cached!r}")
        else:
            print(f"    [bold]CacheTools Version[/]: [cyan2]{cat_ver_cached!r}[/]")
        if isinstance(cot_ver_cached, NoneType):
            print(f"    [bold]ConsoleTools Version[/]: {cot_ver_cached!r}")
        else:
            print(f"    [bold]ConsoleTools Version[/]: [cyan2]{cot_ver_cached!r}[/]")
        if isinstance(dir_ver_cached, NoneType):
            print(f"    [bold]DirectoryTools Version[/]: {dir_ver_cached!r}")
        else:
            print(f"    [bold]DirectoryTools Version[/]: [cyan2]{dir_ver_cached!r}[/]")
        if list_:
            print(']..,')
            self.list_k_v_pairs()
        else:
            print(']')
        if not silent:
            ...
