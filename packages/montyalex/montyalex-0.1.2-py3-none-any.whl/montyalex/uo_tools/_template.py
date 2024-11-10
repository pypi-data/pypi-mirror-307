from abc import abstractmethod
from functools import lru_cache
import msgspec

from montyalex.fs_tools import current_working_dir, joinpaths, pathexists, mkdirs
from montyalex.typing_tools import Any, Dict, Optional


class UserTemplate:
    def __init__(
        self,
        json: bool = False,
        toml: bool = False,
        yaml: bool = False,
        mpck: bool = False,
        directory: str = '.mtax',
        filename: str = 'settings') -> None:
        self._cwd: str = current_working_dir

        self.dirname: str = directory
        self.filename: str = filename

        self.dirpath: str = joinpaths(self._cwd, self.dirname)
        self.filepath: str = joinpaths(self.dirpath, self.filename)

        self._dir_exists: str = pathexists(self.dirpath)
        self._file_exists: str = pathexists(self.filepath)

        selected_formats = [fmt for fmt, enabled in {
            'json': json,
            'toml': toml,
            'yaml': yaml,
            'mpck': mpck
        }.items() if enabled]

        if not selected_formats:
            raise ValueError("At least one format must be enabled (json, toml, yaml, mpck).")

        if len(selected_formats) > 1:
            raise ValueError("Only one format can be enabled at a time.")

        selected_format = selected_formats[0]

        self.modelname = selected_format
        self.modelpath = f'{self.filepath}.{self.modelname}'
        match self.modelname:
            case 'json':
                self.model = self.json
            case 'toml':
                self.model = self.toml
            case 'yaml':
                self.model = self.yaml
            case 'mpck':
                self.model = self.mpck

    @property
    def exists(self) -> bool:
        return pathexists(self.modelpath)

    @property
    @abstractmethod
    def options(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def unpacked(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def items(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def inspect(self):
        raise NotImplementedError

    @lru_cache(maxsize=16)
    def __read_settings(self) -> Dict[str, Any]:
        if pathexists(self.modelpath):
            with open(self.modelpath, 'rb') as settings_file:
                data = settings_file.read()
            if self.modelname == 'json':
                return self._djson(data)
            if self.modelname == 'toml':
                return self._dtoml(data)
            if self.modelname == 'yaml':
                return self._dyaml(data)
            if self.modelname == 'mpck':
                return self._dmpck(data)
        return {}

    def __save_settings(
        self,
        encoded_data: bytes) -> None:
        if not self._dir_exists:
            mkdirs(self.dirpath)
        with open(self.modelpath, 'wb') as settings_file:
            settings_file.write(encoded_data)

    def convert(self, *args, **kwargs):
        msgspec.convert(*args, **kwargs)

    def json(
        self, data: Optional[Any] = None,
        read: bool = False,
        write: bool = False,
        append: bool = False, overwrite: bool = False) -> Dict[str, Any] | None:
        if read:
            return self.__read_settings()
        if write and data is not None:
            self._ejson(data, append=append, overwrite=overwrite)
        return None
    def _ejson(self, data: Dict[str, Any], append: bool = False, overwrite: bool = False) -> None:
        if append:
            existing = self.__read_settings()
            existing.update(data)
            encoded = msgspec.json.encode(existing)
        elif overwrite or not self.exists:
            encoded = msgspec.json.encode(data)
        else:
            encoded = msgspec.json.encode(data)
        encoded = msgspec.json.format(encoded, indent=4)
        self.__save_settings(encoded)
    def _djson(self, *args, **kwargs):
        return msgspec.json.decode(*args, **kwargs)

    def toml(
        self, data: Optional[Any] = None,
        read: bool = False,
        write: bool = False,
        append: bool = False, overwrite: bool = False) -> Dict[str, Any] | None:
        if read:
            return self.__read_settings()
        if write and data is not None:
            self._etoml(data, append=append, overwrite=overwrite)
        return None
    def _etoml(self, data: Dict[str, Any], append: bool = False, overwrite: bool = False) -> None:
        if append:
            existing = self.__read_settings()
            existing.update(data)
            encoded = msgspec.toml.encode(existing)
        elif overwrite or not self.exists:
            encoded = msgspec.toml.encode(data)
        else:
            encoded = msgspec.toml.encode(data)
        self.__save_settings(encoded)
    def _dtoml(self, *args, **kwargs):
        return msgspec.toml.decode(*args, **kwargs)

    def yaml(
        self, data: Optional[Any] = None,
        read: bool = False,
        write: bool = False,
        append: bool = False, overwrite: bool = False) -> Dict[str, Any] | None:
        if read:
            return self.__read_settings()
        if write and data is not None:
            self._eyaml(data, append=append, overwrite=overwrite)
        return None
    def _eyaml(self, data: Dict[str, Any], append: bool = False, overwrite: bool = False) -> None:
        if append:
            existing = self.__read_settings()
            existing.update(data)
            encoded = msgspec.yaml.encode(existing)
        elif overwrite or not self.exists:
            encoded = msgspec.yaml.encode(data)
        else:
            encoded = msgspec.yaml.encode(data)
        self.__save_settings(encoded)
    def _dyaml(self, *args, **kwargs):
        return msgspec.yaml.decode(*args, **kwargs)

    def mpck(
        self, data: Optional[Any] = None,
        read: bool = False,
        write: bool = False,
        append: bool = False, overwrite: bool = False) -> Dict[str, Any] | None:
        if read:
            return self.__read_settings()
        if write and data is not None:
            self._empck(data, append=append, overwrite=overwrite)
        return None
    def _empck(self, data: Dict[str, Any], append: bool = False, overwrite: bool = False) -> None:
        if append:
            existing = self.__read_settings()
            existing.update(data)
            encoded = msgspec.msgpack.encode(existing)
        elif overwrite or not self.exists:
            encoded = msgspec.msgpack.encode(data)
        else:
            encoded = msgspec.msgpack.encode(data)
        self.__save_settings(encoded)
    def _dmpck(self, *args, **kwargs):
        return msgspec.msgpack.decode(*args, **kwargs)


# ---------------------------------------------------------------------------
# | Example Usage
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    standard_user_template = UserTemplate(json=True)
    std_temp = standard_user_template

    d: Dict[str, Any] = {"": ""}
    std_temp.model(d, write=True)
