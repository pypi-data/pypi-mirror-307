from montyalex.console_tools import richconsole
from montyalex.typing_tools import Any
from .category import (
    SettingCategory as Category,
    ACTION,
    DEFAULT,
    USERINFO)

print = richconsole.print


class Settings:
    def __init__(self) -> None:
        self.action: Category = ACTION
        self.default: Category = DEFAULT
        self.userinfo: Category = USERINFO

        self.all: list[Category] = [
            self.action,
            self.default,
            self.userinfo
        ]

    def __str__(self) -> str:
        return f'{self.all}'

    def __repr__(self) -> str:
        return f'Settings({self.all})'

    def get_value(self, key: str, value_only: bool = True) -> Any:
        for category in self.all:
            for subcat in category.subcategories:
                for comp in subcat.components:
                    if f'{comp}' == key:
                        value = comp.get_value()
                        if value_only:
                            return value
                        if f'{comp.parent}' != f'{comp}':
                            return f'mtax.{comp.parent}.{comp}: {value}'
                        return f'mtax.{comp}: {value}'
        return None

    def show_value(self, key: str) -> None:
        for category in self.all:
            for subcat in category.subcategories:
                for comp in subcat.components:
                    if f'{comp}' == key:
                        value = comp.get_value()
                        if f'{comp.parent}' != f'{comp}':
                            print(f'mtax.{comp.parent}.{comp}: {value}')
                        else:
                            print(f'mtax.{comp}: {value}')

    def show_all_values(self) -> None:
        components: list[Category] = []
        for category in self.all:
            for subcat in category.subcategories:
                for component in subcat.components:
                    components.append(component)
        components.sort(
            key=lambda c: (c.parent.prefix.value, c.parent.infix.value, c.parent.suffix.value)
        )
        for comp in components:
            value = comp.get_value()
            type_ = f'{comp.type_}'.removeprefix('<class ').removesuffix('>')
            if f'{comp.parent}' != f'{comp}':
                if value != 'Notfound':
                    print(
                        f'[yellow italic]mtax.[/][orange1]{comp.parent}[/]'
                        f'.[yellow]{comp}[/]: {value!r}'
                    )
                else:
                    print(
                        f'[yellow italic]mtax.[/][orange1]{comp.parent}[/]'
                        f'.[yellow]{comp}[/]: [red]{value}[/]'
                        f'[dim] (Value should be of type {type_})[/]'
                    )
            else:
                if value != 'Notfound':
                    print(f'[yellow italic]mtax.[/][yellow]{comp}[/]: {value!r}')
                else:
                    print(
                        f'[yellow italic]mtax.[/][yellow]{comp}[/]: [red]{value}[/]'
                        f'[dim] (Value should be of type {type_})[/]'
                    )


# ----------------------------------------------------------------------
# | Global Settings Object
# ----------------------------------------------------------------------
SETTINGS = Settings()
