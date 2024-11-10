from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent)


# ----------------------------------------------------------------------
# | UserInfo
# ----------------------------------------------------------------------
class UserInfo(SettingComponent):
    def __init__(
        self,
        infix: str,
        suffix: str,
        type_: type,
        *,
        prefix: str = 'user',
        parent: GroupSettingName | ShortSettingName | SettingName = None) -> None:
        super().__init__(prefix, infix, suffix, type_=type_, parent=parent)


# ----------------------------------------------------------------------
# | Locale
# ----------------------------------------------------------------------
locale_continent_userinfo = UserInfo(
    'locale', 'continent', str, parent=SettingName('user', 'locale', 'continent'))
locale_country_userinfo = UserInfo(
    'locale', 'country', str, parent=SettingName('user', 'locale', 'country'))
locale_region_userinfo = UserInfo(
    'locale', 'region', str, parent=SettingName('user', 'locale', 'region'))
locale_state_userinfo = UserInfo(
    'locale', 'state', str, parent=SettingName('user', 'locale', 'state'))
locale_province_userinfo = UserInfo(
    'locale', 'province', str, parent=SettingName('user', 'locale', 'province'))
locale_city_userinfo = UserInfo('locale', 'city', str, parent=SettingName('user', 'locale', 'city'))
locale_streetname_userinfo = UserInfo(
    'locale', 'street-name', str, parent=SettingName('user', 'locale', 'street-name'))
locale_streetnum_userinfo = UserInfo(
    'locale', 'street-number', str, parent=SettingName('user', 'locale', 'street-number'))
