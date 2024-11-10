from ._components import (
    GroupSettingName as Group)
from .subcategory import (
    SettingSubcategory as Subcategory,
    option_action_subcategory,
    info_default_subcategory,
    option_default_subcategory,
    locale_userinfo_subcategory)


# ----------------------------------------------------------------------
# | SettingCategory
# ----------------------------------------------------------------------
class SettingCategory:
    def __init__(self, prefix: str, type_: type, *subcategories: Subcategory) -> None:
        self.info: Group = Group(prefix)
        self.type_: type = type_
        self.subcategories: tuple[Subcategory] = subcategories

    def __str__(self) -> str:
        return f'{self.subcategories}'

    def __repr__(self) -> str:
        subcategories = f'{list(self.subcategories)!r}'
        return f'Category(={self.info.prefix}, type={self.type_}, subcategories={subcategories})'

    def add_subcategory(self, subcategory: Subcategory) -> None:
        new_subcategories = (*self.subcategories, subcategory)
        self.subcategories = new_subcategories


# ----------------------------------------------------------------------
# | Categories
# ----------------------------------------------------------------------
ACTION = SettingCategory('action', object, option_action_subcategory)
DEFAULT = SettingCategory('default', object, info_default_subcategory, option_default_subcategory)
USERINFO = SettingCategory('user', object, locale_userinfo_subcategory)
