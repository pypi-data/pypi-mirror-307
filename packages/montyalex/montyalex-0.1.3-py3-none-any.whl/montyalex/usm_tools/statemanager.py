from montyalex.console_tools import richconsole
from montyalex.fs_tools import cancel
from montyalex.object_tools import (
    Key,
    Value,
    MontyKeyValueError as KeyValError,
    MontyJSONError as JSONDecoderError,
    MontyRangeError as RangeError)
from montyalex.typing_tools import Any, Literal
from montyalex.uo_tools import yaml

print = richconsole.print


class State:
    def __init__(
        self,
        file_name: str,
        *,
        multiplier: int = 1,
        limit: int | tuple[int, int] = None,
        ilimit: int | tuple[int, int] = None,
        loc: str = '.mtax') -> None:
        __yaml = yaml(directory=loc, filename=file_name)
        self.multiplier: int = multiplier
        self.limit: int | tuple[int, int] = limit
        self.ilimit: int | tuple[int, int] = ilimit
        self.file_name: str = file_name
        self.file_path: str = f'{file_name}.{__yaml.modelname}'
        self.full_path: str = __yaml.modelpath
        self.loc: str = loc
        self.yamlchange = __yaml.change
        self.yamlexists = __yaml.exists
        self.yamlmodel = __yaml.model
        self.yamlremove = __yaml.remove

    def get(self, key: Key):
        key_value = self.get_value(key)
        if key_value is not None:
            state: dict[Key, Any] = {key: key_value}
            print(f'Key Found {state}')
        else:
            raise KeyValError('No value associated')

    def get_value(self, key: Key):
        try:
            key_value = self.yamlmodel(read=True)[key]
            if key_value is not None:
                return key_value
            raise KeyValError(f'Null assignment for {key!r}; no value associated with active state')
        except (KeyError, TypeError, JSONDecoderError):
            print(f"KeyError: {key!r} can not be found in file; no value was assigned")
            return None

    def delete(self, key: Key = None, value: Value = None, *, fulloc: bool = False):
        if key is None and value is None:
            path = self.file_path
            if fulloc:
                path = self.full_path
            if self.yamlexists:
                self.yamlremove()
                print(f"Removed {path!r}")
            else:
                raise FileNotFoundError(f'the state file {path!r} is missing')
        if key and not value:
            key_value = self.get_value(key)
            state: dict[Key, Any] = {key: key_value}
            if key_value is not None:
                print(f"Removed {state} from {self.file_name!r}")
                self.yamlchange(key, None)
            else:
                raise KeyValError(
                    f"{key!r} was not nullified {state}, no value exists for defined key")
        if key and value:
            key_value = self.get_value(key)
            state: dict[Key, Any] = {key: value}
            if key_value == value:
                print(f"Removed {state} from {self.file_name!r}")
                self.yamlchange(key, None)
            else:
                raise KeyValError(
                    f"{key!r} was not nullified {state}, value ({value!r}) does not match")

    def manager(self, key: Key, value: Value):
        state: dict[Key, Any] = {key: value}
        print(f"State Changed {state}")
        if self.yamlexists and self.get_value(key):
            self.yamlmodel(state, write=True, append=True)
        else:
            self.yamlmodel(state, write=True)

    def _modifier(
        self,
        value: Value,
        operation: Literal[0] | Literal[1] | Literal[2] | Literal[3],
        *,
        batch: int):
        check = value
        if value is not None:
            check = value + self.multiplier if operation == 0 else value - self.multiplier
            if operation == 2:
                check = value + batch
            if operation == 3:
                check = value - batch
            if check % batch != 0:
                check = f'{check}, batch % {batch} != 0'
        if check is None:
            check = f'±0, {{{operation}, {value}*{self.multiplier}}}'
        if isinstance(self.limit, tuple) or isinstance(self.ilimit, tuple):
            inclusive_limit = range(self.ilimit[0], self.ilimit[1] + 1)
            range_limit = range(*self.limit) if not self.ilimit else inclusive_limit
            if value not in range_limit or check not in range_limit:
                if self.limit:
                    raise RangeError(f'Index ({check}) not in', range(*self.limit))
                if self.ilimit:
                    raise RangeError(f'Index ({check}) not in', range(*self.ilimit))
                cancel()
        if isinstance(self.limit, int) or isinstance(self.ilimit, int):
            range_limit = range(self.limit) if not self.ilimit else range(self.ilimit + 1)
            if value not in range_limit or check not in range_limit:
                if self.limit:
                    raise RangeError(f'Index ({check}) not in', range(self.limit))
                if self.ilimit:
                    raise RangeError(f'Index ({check}) not in', range(self.ilimit))
                cancel()
        return True

    def decr(self, key: Key):
        key_value = self.get_value(key)
        old_state: dict[Key, Any] = {key: key_value}
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value - self.multiplier}
        try:
            smdecr = self._modifier(key_value, 1, batch=self.multiplier)
            if state[key] != key_value and smdecr:
                print(f"Decremented {old_state} -> {state}")
                self.yamlmodel(state, write=True, append=True)
        except (KeyValError, RangeError) as e:
            print(e)

    def incr(self, key: Key):
        key_value = self.get_value(key)
        old_state: dict[Key, Any] = {key: key_value}
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value + self.multiplier}
        try:
            smincr = self._modifier(key_value, 0, batch=self.multiplier)
            if state[key] != key_value and smincr:
                print(f"Incremented {old_state} -> {state}")
                self.yamlmodel(state, write=True, append=True)
        except (KeyValError, RangeError) as e:
            print(e)

    def bypass(self, key: Key, batch: int):
        key_value = self.get_value(key)
        old_state: dict[Key, Any] = {key: key_value}
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value + batch}
        try:
            smbatch = self._modifier(key_value, 2, batch=batch)
            if state[key] != key_value and smbatch:
                print(f"Incremented {old_state} -> (batch={batch}) -> {state}")
                self.yamlmodel(state, write=True, append=True)
        except (KeyValError, RangeError) as e:
            print(e)

    def nbypass(self, key: Key, batch: int):
        key_value = self.get_value(key)
        old_state: dict[Key, Any] = {key: key_value}
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value - batch}
        try:
            smbatch = self._modifier(key_value, 3, batch=batch)
            if state[key] != key_value and smbatch:
                print(f"Decremented {old_state} -> (batch={batch}) -> {state}")
                self.yamlmodel(state, write=True, append=True)
        except (KeyValError, RangeError) as e:
            print(e)

    def toggle(self, key: Key, *, on: bool = False, off: bool = False):
        self.multiplier = 2
        self.ilimit = (-1, 1)
        key_value = self.get_value(key)
        old_state: dict[Key, Any] = {key: '[green]on[/]' if key_value == 1 else '[red]off[/]'}
        state: dict[Key, Any] = {}
        state_repr: dict[Key, Any] = {}
        if on:
            if isinstance(key_value, int):
                state: dict[Key, Any] = {key: 1}
                state_repr: dict[Key, Any] = {key: '[green]on[/]'}
            try:
                if state[key] != key_value:
                    print(f"Toggled {old_state} -> {state_repr}")
                    self.yamlmodel(state, write=True, append=True)
            except (KeyValError, RangeError) as e:
                print(e)
        if off:
            if isinstance(key_value, int):
                state: dict[Key, Any] = {key: -1}
                state_repr: dict[Key, Any] = {key: '[red]off[/]'}
            try:
                if state[key] != key_value:
                    print(f"Toggled {old_state} -> {state_repr}")
                    self.yamlmodel(state, write=True, append=True)
            except (KeyValError, RangeError) as e:
                print(e)
