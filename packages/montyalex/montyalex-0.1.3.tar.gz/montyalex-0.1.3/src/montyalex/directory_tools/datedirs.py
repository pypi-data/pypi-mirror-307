from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from montyalex.cache_tools import add_to_cache, remove_item_from_cache
from montyalex.console_tools import richconsole, success_stm
from montyalex.fs_tools import abspath, current_working_dir, joinpaths, mkdirs, pathexists
from montyalex.us_tools import datetime_format_option_default
from .helpdirs import remove_formatted__dir

print = richconsole.print


FORMAT = datetime_format_option_default.get_value()
if FORMAT == 'Notfound':
    FORMAT = '%Y-%m-%d'
START = datetime.now()

def create_date_directories(
        range_: int = 1, four_weeks: bool = False, parent: str = None, silent: bool = False):
    add_to_cache(key='_datedirs_', value=f'{START:FORMAT}', silent=True)
    new_date = START
    for i in range(range_ * 12):
        if four_weeks:
            new_date += timedelta(days=28)
        else:
            new_date = START + relativedelta(months=i)
        formatted_date = new_date.strftime(FORMAT)
        if parent:
            mkdirs(joinpaths(current_working_dir, parent, formatted_date), exist_ok=True)
        else:
            mkdirs(joinpaths(current_working_dir, formatted_date), exist_ok=True)
        if not silent:
            cwd_ = abspath(parent) if parent else current_working_dir
            print(
                f'{success_stm}, Created {formatted_date!r} in {cwd_!r}')

def remove_date_directories(
        range_: int = 1, four_weeks: bool = False, parent: str = None, silent: bool = False):
    remove_item_from_cache(key='_datedirs_', silent=True)
    if parent:
        remove_formatted__dir(parent, silent)

        new_date = START
        for i in range(range_ * 12):
            if four_weeks:
                new_date += timedelta(days=28)
            else:
                new_date = START + relativedelta(months=i)
            formatted_date = new_date.strftime('%Y-%m-%d')
            formatted_directory = joinpaths(current_working_dir, formatted_date)
            formatted_directory = joinpaths(current_working_dir, parent)
            if not pathexists(formatted_directory) and not silent:
                print(
                    f'{success_stm}, Removed {formatted_date!r} from {formatted_directory!r}')
        if not pathexists(parent) and not silent:
            print(f'{success_stm}, Removed {parent!r} from {current_working_dir!r}')
    else:
        for i in range(range_ * 12):
            new_date = START + relativedelta(months=i)
            formatted_date = new_date.strftime('%Y-%m-%d')
            formatted_directory = joinpaths(current_working_dir, formatted_date)
            remove_formatted__dir(formatted_directory, silent)
            if not pathexists(formatted_directory) and not silent:
                print(f'{success_stm}, Removed {formatted_date!r} from {current_working_dir!r}')
