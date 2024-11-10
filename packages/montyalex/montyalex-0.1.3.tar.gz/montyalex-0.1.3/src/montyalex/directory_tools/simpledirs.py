from montyalex.console_tools import richconsole, success_stm
from montyalex.fs_tools import current_working_dir, joinpaths, mkdirs, pathexists
from .helpdirs import remove_formatted__dir

print = richconsole.print


def create_simple_directories(
    range_: int = 1,
    name_: str = None,
    prefix: str = None,
    suffix: str = None,
    silent: bool = False):
    for i in range(range_):
        formatted_directory_name = name_ if name_ else f'{i:03}'
        if prefix:
            formatted_directory_name = f'{prefix}{formatted_directory_name}'
        if suffix:
            formatted_directory_name = f'{formatted_directory_name}{suffix}'
        mkdirs(joinpaths(current_working_dir, formatted_directory_name), exist_ok=True)
        if not silent:
            print(
                f'{success_stm}, Created {formatted_directory_name!r} in {current_working_dir!r}')

def remove_simple_directories(
    range_: int = 1,
    name_: str = None,
    prefix: str = None,
    suffix: str = None,
    silent: bool = False):
    for i in range(range_):
        formatted_directory_name = name_ if name_ else f'{i:03}'
        if prefix:
            formatted_directory_name = f'{prefix}{formatted_directory_name}'
        if suffix:
            formatted_directory_name = f'{formatted_directory_name}{suffix}'
        formatted_directory = joinpaths(current_working_dir, formatted_directory_name)
        remove_formatted__dir(formatted_directory, silent)

        if not pathexists(formatted_directory) and not silent:
            print(
                f'{success_stm}, Removed {formatted_directory_name!r} from {current_working_dir!r}')
