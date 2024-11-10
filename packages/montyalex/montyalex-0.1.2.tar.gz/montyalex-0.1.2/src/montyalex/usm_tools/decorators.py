from montyalex.fs_tools import cancel
from montyalex.object_tools import Key, Value, MontyRangeError as RangeError
from montyalex.typing_tools import Any, Literal
from montyalex.uo_tools import yaml


def statemanager_decorator(
        key: Key,
        value: Value,
        file_name: str,
        *,
        loc: str = None):
    yaml_state = yaml(directory=loc if loc else '.mtax', filename=file_name)
    def statemanager(func):
        state: dict[Key, Any] = {key: value}
        def wrapper():
            print(f"{state}")
            func()
        yaml_state.model(state, write=True, overwrite=True)
        return wrapper
    print(yaml_state.modelpath)
    return statemanager

def statemodifier(
    value: Value,
    operation: Literal[0] | Literal[1],
    multiplier: int = 1,
    limit: int | tuple[int, int] = None,
    ilimit: int | tuple[int, int] = None):
    if isinstance(limit, tuple) or isinstance(ilimit, tuple):
        range_limit = range(*limit) if not ilimit else range(ilimit[0], ilimit[1] + 1)
        check = value + multiplier if operation == 0 else value - multiplier
        if value not in range_limit or check not in range_limit:
            if limit:
                raise RangeError(f'Index ({check}) not in', range(*limit))
            if ilimit:
                raise RangeError(f'Index ({check}) not in', range(*ilimit))
            cancel()
    if isinstance(limit, int) or isinstance(ilimit, int):
        range_limit = range(limit) if not ilimit else range(ilimit + 1)
        check = value + multiplier if operation == 0 else value - multiplier
        if value not in range_limit or check not in range_limit:
            if limit:
                raise RangeError(f'Index ({check}) not in', range(limit))
            if ilimit:
                raise RangeError(f'Index ({check}) not in', range(ilimit))
            cancel()
    return True

def statedecr_decorator(
        key: Key,
        file_name: str,
        *,
        multiplier: int = 1,
        limit: int | tuple[int, int] = None,
        ilimit: int | tuple[int, int] = None,
        loc: str = None):
    yaml_state = yaml(directory=loc if loc else '.mtax', filename=file_name)
    def statedecrementer(func):
        key_value = yaml_state.model(read=True)[key]
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value - multiplier}
        def wrapper():
            func()
        try:
            smdecr = statemodifier(key_value, 1, multiplier, limit, ilimit)
            if state[key] != key_value and smdecr:
                print(f"{state}")
                yaml_state.model(state, write=True, overwrite=True)
                print(yaml_state.modelpath)
        except RangeError as e:
            print(e)
        return wrapper
    return statedecrementer

def stateincr_decorator(
        key: Key,
        file_name: str,
        *,
        multiplier: int = 1,
        limit: int | tuple[int, int] = None,
        ilimit: int | tuple[int, int] = None,
        loc: str = None):
    yaml_state = yaml(directory=loc if loc else '.mtax', filename=file_name)
    def stateincrementer(func):
        key_value = yaml_state.model(read=True)[key]
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value + multiplier}
        def wrapper():
            func()
        try:
            smincr = statemodifier(key_value, 0, multiplier, limit, ilimit)
            if state[key] != key_value and smincr:
                print(f"{state}")
                yaml_state.model(state, write=True, overwrite=True)
                print(yaml_state.modelpath)
        except RangeError as e:
            print(e)
        return wrapper
    return stateincrementer
