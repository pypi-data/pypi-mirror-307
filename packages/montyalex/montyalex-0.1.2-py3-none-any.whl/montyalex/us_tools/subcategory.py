from ._components import (
    ShortSettingName as Short,
    SettingComponent as Component)
from ._actions import (
    silent_option_action)
from ._defaults import (
    datetime_range_option_default,
    datetime_format_option_default,
    timeout_option_default,
    fourweek_option_default,
    simple_range_option_default,
    timezone_info_default)
from ._userinfo import (
    locale_city_userinfo,
    locale_continent_userinfo,
    locale_country_userinfo,
    locale_province_userinfo,
    locale_region_userinfo,
    locale_state_userinfo,
    locale_streetname_userinfo,
    locale_streetnum_userinfo)


# ----------------------------------------------------------------------
# | SettingSubcategory
# ----------------------------------------------------------------------
class SettingSubcategory:
    def __init__(self, prefix: str, infix: str, type_: type, *components: Component) -> None:
        self.info: Short = Short(prefix, infix)
        self.type_: type = type_
        self.components: tuple[Component] = components

    def __str__(self) -> str:
        return f'{self.components}'

    def __repr__(self) -> str:
        return (
            f'Subcategory(={self.info.prefix}.{self.info.infix}, '
            f'type={self.type_}, components={list(self.components)!r})'
        )

    def add_component(self, component: Component) -> None:
        new_components = (*self.components, component)
        self.components = new_components


# ----------------------------------------------------------------------
# | Subcategories
# ----------------------------------------------------------------------
option_action_subcategory = SettingSubcategory('action', 'opt', object, silent_option_action)
info_default_subcategory = SettingSubcategory('default', 'info', object, timezone_info_default)
option_default_subcategory = SettingSubcategory('default', 'opt', object,
    timeout_option_default,
    fourweek_option_default,
    datetime_range_option_default,
    datetime_format_option_default,
    simple_range_option_default)
locale_userinfo_subcategory = SettingSubcategory('user', 'locale', object,
    locale_region_userinfo,
    locale_continent_userinfo,
    locale_country_userinfo,
    locale_state_userinfo,
    locale_province_userinfo,
    locale_city_userinfo,
    locale_streetname_userinfo,
    locale_streetnum_userinfo)
