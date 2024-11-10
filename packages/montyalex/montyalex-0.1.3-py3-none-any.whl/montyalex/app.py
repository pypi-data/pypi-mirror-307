from ._mtax import mtax_blueprints, mtax_commands, mtax_complete, mtax_funcargs
from ._settings import settings_
from .cache_tools import cache_, incr_in_cache, decr_in_cache
from .fs_tools import cancel
from .console_tools import richconsole, warn_stm
from .directory_tools import (
    datedirs, rmdatedirs, simpledirs, rmsimpledirs)
from .time_tools import func_time
from .typing_tools import NoneType
from .typer_tools import Option, Typer

print = richconsole.print



monty: Typer = Typer(
    name='monty',
    add_help_option=False,
    pretty_exceptions_show_locals=False)
monty.add_typer(settings_)
monty.add_typer(cache_)
LINEDASH = '___________________________________________________________________________________'

def date_dirs__helper(name_: str, prefix: str, suffix: str, silent: bool = False):
    if (name_ or prefix or suffix) and not silent:
        print('Not allowed with the -datedirs option')
        cancel()

@monty.command(name='mk')
@func_time('to create the directories')
def create__dirs(
    range_: int = Option(1, '--range', '-r'),
    s_dirs: bool = Option(
        False, '--simple-directories', '-dirs', is_flag=True, show_default='range: 1'),
    dt_dirs: bool = Option(
        False, '--date-directories', '-datedirs', is_flag=True, show_default='range: 1yr'),
    four_weeks: bool = Option(False, '--four-weeks', '-4w', is_flag=True),
    dir_parent: str = Option(None, '--parent', '-p'),
    dir_name: str = Option(None, '--name'),
    prefix: str = Option(None, '--prefix'),
    suffix: str = Option(None, '--suffix'),
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Creates new folders in the current local directory"""
    if s_dirs:
        simpledirs(range_, dir_name, prefix, suffix, silent)
        incr_in_cache(key='_mkdirs', silent=silent)
    if dt_dirs:
        date_dirs__helper(dir_name, prefix, suffix, silent)
        datedirs(range_, four_weeks, dir_parent, silent)
        incr_in_cache(key='_mkdates', silent=silent)
    if not s_dirs and not dt_dirs:
        print('Void, Please provide a type of directory to make')

@monty.command(name='rm')
@func_time('to remove the directories')
def remove__dirs(
    range_: int = Option(1, '--range', '-r'),
    s_dirs: bool = Option(
        False, '--simple-directories', '-dirs', is_flag=True, show_default='range: 1'),
    dt_dirs: bool = Option(
        False, '--date-directories', '-datedirs', is_flag=True, show_default='range: 1yr'),
    four_weeks: bool = Option(False, '--four-weeks', '-4w', is_flag=True),
    dir_parent: str = Option(None, '--parent', '-p'),
    dir_name: str = Option(None, '--name', show_default='000'),
    prefix: str = Option(None, '--prefix'),
    suffix: str = Option(None, '--suffix'),
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extraneous messages in console')):
    """Removes folders in the current local directory"""
    if s_dirs:
        rmsimpledirs(range_, dir_name, prefix, suffix, silent)
        decr_in_cache(key='_mkdirs', silent=silent)
    if dt_dirs:
        date_dirs__helper(dir_name, prefix, suffix, silent)
        rmdatedirs(range_, four_weeks, dir_parent, silent)
        decr_in_cache(key='_mkdates', silent=silent)
    else:
        print('Void, Please provide a type of directory to remove')

def __commands_help(split: bool = False, commands: bool = False):
    if commands:
        if split:
            print('')
        print('cmds.')
        if split:
            print('')
        for name, shorthelp, index, defaults in mtax_commands:
            if isinstance(index, int):
                if index <= 9:
                    command_help = f"([pink3 dim]{index}[/]) {name} -> [dim italic]{shorthelp}[/]"
                else:
                    command_help = f"([pink3 dim]{index}[/]){name} -> [dim italic]{shorthelp}[/]"
            if isinstance(index, NoneType):
                command_help = f"([dim]X[/]) {name} -> [dim italic]{shorthelp}[/]"
            if defaults:
                command_help += f' [pink3 dim italic]({defaults})[/]'
            print(command_help)
            if split:
                print('')

def __funcargs_help(split: bool = False, func_args: bool = False):
    if func_args:
        if split:
            print('')
        print('args.')
        if split:
            print('')
        for func, module, funcargs_index, funcargs_defaults in mtax_funcargs:
            if funcargs_index:
                if funcargs_index != '.':
                    funcargs_help = f"([green1 dim]{funcargs_index}[/]) [italic]{func}[/]"
                else:
                    funcargs_help = f"([dim]{funcargs_index}[/]) [italic]{func}[/]"
            else:
                funcargs_help = f"    [italic]{func}[/]"
            if module:
                funcargs_help += f' -> [green1 dim italic]{module}[/]'
            if funcargs_defaults:
                funcargs_help += f' [dim italic]({funcargs_defaults})[/]'
            if not module and not funcargs_defaults:
                funcargs_help += ' [dim italic]...[/]'
            print(funcargs_help)
            if split:
                print('')

def __blueprints_help(split: bool = False, blueprints: bool = False):
    if blueprints:
        if split:
            print('')
        print('bpns.')
        if split:
            print('')
        for blueprint, module, blueprint_index, blueprint_defaults in mtax_blueprints:
            if blueprint_index:
                blueprint_help = f"([blue3 dim]{blueprint_index}[/]) {blueprint}"
            else:
                blueprint_help = f"    {blueprint}"
            if module:
                blueprint_help += f' -> [blue3 dim italic]{module}[/]'
            if blueprint_defaults:
                blueprint_help += f' [dim italic]({blueprint_defaults})[/]'
            if not module and not blueprint_defaults:
                blueprint_help += ' [dim italic]...[/]'
            print(blueprint_help)
            if split:
                print('')

@monty.command()
@monty.command(name='help')
@cache_.command(name='help')
@settings_.command(name='help')
def mtax(
    help_: bool = Option(False, '--help', '-h'),
    split: bool = Option(False, '--split'),
    save_funcargs_to_file: bool = Option(False, '--save-a', '-s-a'),
    save_blueprints_to_file: bool = Option(False, '--save-b', '-s-b'),
    save_commands_to_file: bool = Option(False, '--save-c', '-s-c'),
    save_file: bool = Option(False, '--save'),
    func_args: bool = Option(False, '-a', '--args'),
    blueprints: bool = Option(False, '-b', '--blueprints'),
    commands: bool = Option(False, '-c', '--commands'),
    super_silence: bool = Option(False, '-ss'),
    silence: bool = Option(False, '-s')):
    """."""
    if help_:
        print('HELP')
    else:
        if not super_silence:
            print(LINEDASH)
            __commands_help(split, (not blueprints and not func_args) or commands)
            if (func_args or blueprints) and commands:
                print(LINEDASH)
            __funcargs_help(split, func_args)
            if func_args and blueprints:
                print(LINEDASH)
            __blueprints_help(split, blueprints)
            print(LINEDASH)
        if save_commands_to_file:
            mtax_complete(commands=True, func_args=False, blueprints=False)
        if save_funcargs_to_file:
            mtax_complete(commands=False, func_args=True, blueprints=False)
        if save_blueprints_to_file:
            mtax_complete(commands=False, func_args=False, blueprints=True)
        if save_file:
            mtax_complete(commands=commands, func_args=func_args, blueprints=blueprints)
            if not silence and not super_silence:
                print(f'{warn_stm}, Syntax highlighting is not supported in files')
