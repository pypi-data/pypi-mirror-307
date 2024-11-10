from abc import abstractmethod
from functools import total_ordering
from json import JSONDecodeError

from montyalex.fs_tools import pathexists, joinpaths, current_working_dir
from montyalex.typing_tools import Any
from montyalex.uo_tools import json, toml, yaml, mpck


class _Prefix:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'Prefix({self.value})'

class _Infix:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'Infix({self.value})'

class _Suffix:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'Suffix({self.value})'

@total_ordering
class GroupSettingName:
    def __init__(self, prefix: str) -> None:
        self.prefix: _Prefix = _Prefix(prefix)

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        return self.prefix.value == other.prefix.value

    @abstractmethod
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        if self.prefix.value < other.prefix.value:
            return True
        return False

    @abstractmethod
    def __hash__(self):
        return hash((self.prefix.value))

@total_ordering
class ShortSettingName(GroupSettingName):
    def __init__(self, prefix: str, infix: str) -> None:
        super().__init__(prefix)
        self.infix: _Infix = _Infix(infix)

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        return (self.prefix.value, self.infix.value) == (other.prefix.value, other.infix.value)

    @abstractmethod
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        if self.prefix.value < other.prefix.value:
            return True
        if self.prefix.value > other.prefix.value:
            return False
        return self.infix.value < other.infix.value

    @abstractmethod
    def __hash__(self):
        return hash((self.prefix.value, self.infix.value))

class SettingName(ShortSettingName):
    def __init__(self, prefix: str, infix: str, suffix: str) -> None:
        super().__init__(prefix, infix)
        self.suffix: _Suffix = _Suffix(suffix)

    def __str__(self) -> str:
        return f'{self.prefix}.{self.infix}.{self.suffix}'

    def __repr__(self) -> str:
        return f'Name({self.prefix}.{self.infix}.{self.suffix})'

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        return (self.prefix.value, self.infix.value) == (other.prefix.value, other.infix.value)

    @abstractmethod
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SettingName):
            return NotImplemented
        if self.prefix.value < other.prefix.value:
            return True
        if self.prefix.value > other.prefix.value:
            return False
        if self.infix.value < other.infix.value:
            return True
        if self.infix.value > other.infix.value:
            return False
        return self.suffix.value < other.suffix.value

    @abstractmethod
    def __hash__(self):
        return hash((self.prefix.value, self.infix.value, self.suffix.value))

class SettingComponent(SettingName):
    def __init__(
        self, prefix: str, infix: str, suffix: str,
        *,
        parent: (GroupSettingName | ShortSettingName | SettingName) = None,
        type_: type) -> None:
        super().__init__(prefix, infix, suffix)
        self.parent: GroupSettingName | ShortSettingName | SettingName = parent
        self.type_: type = type_
        self.value: str | bool | int | None = None

    def __str__(self) -> str:
        return f'{self.prefix}.{self.infix}.{self.suffix}'

    def __repr__(self) -> str:
        if self.get_value() != 'Notfound':
            return f'Component(={self!s}, type={self.type_}, value={self.get_value()!r})'
        return f'Component(={self!s}, type={self.type_}, value={self.get_value()})'

    def __eq__(self, other: object) -> bool:
        parent_name = f"{self.parent.prefix}.{self.parent.infix}.{self.parent.suffix}"
        if parent_name != f"{self!s}":
            if not isinstance(other, SettingName):
                return NotImplemented
            return (self.prefix.value, self.infix.value) == (other.prefix.value, other.infix.value)
        if not isinstance(other, SettingName):
            return NotImplemented
        return (self.parent.prefix.value, self.parent.infix.value) == \
            (other.parent.prefix.value, other.parent.infix.value)

    def __lt__(self, other: object) -> bool:
        parent_name = f"{self.parent.prefix}.{self.parent.infix}.{self.parent.suffix}"
        if parent_name != f"{self!s}":
            if not isinstance(other, SettingName):
                return NotImplemented
            if self.prefix.value < other.prefix.value:
                return True
            if self.prefix.value > other.prefix.value:
                return False
            if self.infix.value < other.infix.value:
                return True
            if self.infix.value > other.infix.value:
                return False
            return self.suffix.value < other.suffix.value
        if not isinstance(other, SettingName):
            return NotImplemented
        if self.parent.prefix.value < other.parent.prefix.value:
            return True
        if self.parent.prefix.value > other.parent.prefix.value:
            return False
        if self.parent.infix.value < other.parent.infix.value:
            return True
        if self.parent.infix.value > other.parent.infix.value:
            return False
        return self.parent.suffix.value < other.parent.suffix.value

    def __hash__(self):
        return hash((self.prefix.value, self.infix.value, self.suffix.value))

    def get_value(self) -> Any:
        uo: json | toml | yaml | mpck | None = None
        uo_exists = False
        if pathexists(joinpaths(current_working_dir, '.mtax', 'settings.json')):
            uo = json()
        if pathexists(joinpaths(current_working_dir, '.mtax', 'settings.toml')):
            uo = toml()
        if pathexists(joinpaths(current_working_dir, '.mtax', 'settings.yaml')):
            uo = yaml()
        if pathexists(joinpaths(current_working_dir, '.mtax', 'settings.mpck')):
            uo = mpck()
        if uo is None:
            uo = json()
        uo_exists = uo.exists

        mtax_obj = None
        parent_name = f"{self.parent.prefix}.{self.parent.infix}.{self.parent.suffix}"
        if uo_exists:
            try:
                if parent_name != f"{self!s}":
                    mtax_obj = uo.model(
                        read=True
                    )["mtax"][f"{parent_name}"][f"{self!s}"]
                else:
                    mtax_obj = uo.model(
                        read=True
                    )["mtax"][f"{self!s}"]
            except (KeyError, JSONDecodeError):
                return 'Notfound'
        if mtax_obj is not None:
            return mtax_obj
        return 'Notfound'
