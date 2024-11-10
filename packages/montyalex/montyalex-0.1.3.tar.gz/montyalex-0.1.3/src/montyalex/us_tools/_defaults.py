from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent)
from ._actions import datetime_directory_action, simple_directory_action


# ----------------------------------------------------------------------
# | Default
# ----------------------------------------------------------------------
class Default(SettingComponent):
    def __init__(
        self,
        infix: str,
        suffix: str,
        type_: type,
        *,
        prefix: str = 'default',
        parent: GroupSettingName | ShortSettingName | SettingName = None) -> None:
        super().__init__(prefix, infix, suffix, type_=type_, parent=parent)


# ----------------------------------------------------------------------
# | Defaults
# ----------------------------------------------------------------------
timezone_info_default = Default(
    'info', 'timezone', str, parent= SettingName('default', 'info', 'timezone'))
timeout_option_default = Default(
    'opt', 'timeout', str, parent=SettingName('default', 'opt', 'timeout'))
fourweek_option_default = Default('opt', 'four-week-month', bool, parent=datetime_directory_action)
datetime_range_option_default = Default('opt', 'range', str, parent=datetime_directory_action)
datetime_format_option_default = Default('opt', 'format', str, parent=datetime_directory_action)
simple_range_option_default = Default('opt', 'range', str, parent=simple_directory_action)
