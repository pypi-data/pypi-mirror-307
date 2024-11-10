from rich.console import Console


richconsole: Console = Console(highlight=False)
success_stm: str = '[green]Success![/]'
info_stm: str = '[blue1]Info![/]'
warn_stm: str = '[red]Warning![/]'
error_stm: str = '[red]Error![/]'
debug_stm: str = '[orange1]Debug![/]'
critical_stm: str = '[red]Critical![/]'

__version__ = 'v1.0.0'


__all__ = [
    "richconsole",
    "success_stm",
    "info_stm",
    "warn_stm",
    "error_stm",
    "debug_stm",
    "critical_stm",
    "__version__"]
