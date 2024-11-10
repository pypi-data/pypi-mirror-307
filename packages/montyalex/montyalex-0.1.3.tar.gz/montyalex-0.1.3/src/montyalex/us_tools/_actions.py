from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent)


# ----------------------------------------------------------------------
# | Action
# ----------------------------------------------------------------------
class Action(SettingComponent):
    def __init__(
        self,
        infix: str,
        suffix: str,
        type_: type,
        *,
        prefix: str = 'action',
        parent: GroupSettingName | ShortSettingName | SettingName = None) -> None:
        super().__init__(prefix, infix, suffix, type_=type_, parent=parent)


# ----------------------------------------------------------------------
# | Actions
# ----------------------------------------------------------------------
datetime_directory_action = Action(
    'dirs', 'datetime', object, parent=SettingName('action', 'dirs', 'datetime'))
simple_directory_action = Action(
    'dirs', 'simple', object, parent=SettingName('action', 'dirs', 'simple'))
silent_option_action = Action('opt', 'silent', bool, parent=SettingName('action', 'opt', 'silent'))
