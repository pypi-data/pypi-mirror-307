import shutil

from montyalex.console_tools import richconsole, error_stm
from montyalex.fs_tools import pathexists

print = richconsole.print


def remove_formatted__dir(formatted_directory: str | bytes, silent: bool = False) -> bool:
    if pathexists(formatted_directory):
        try:
            shutil.rmtree(formatted_directory)
            return True
        except (OSError, NotADirectoryError, IsADirectoryError):
            if not silent:
                print(
                    f'{error_stm}, Removing {formatted_directory!r} failed in the directory given')
            return False
    else:
        if not silent:
            print(
                f'Warning, Attempted to remove {formatted_directory!r}, ' + "but it didn't exist")
        return False
