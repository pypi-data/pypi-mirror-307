#  TO DO by 2024/11/30
from montyalex.fs_tools import (
    # abspath,  # maybe be used
    cancel,
    expanduser,
    joinpaths,
    # mkfile,  # maybe be used
    rmfile,
    # mkdirs,  # maybe be used
    # rmdirs,  # maybe be used
    # rmtree,  # maybe be used
    pathexists,
    current_working_dir as curr_workdir  # possible renaming of variable namespace
)
from montyalex.time_tools import MtaxTime
from montyalex.typing_tools import Any
from montyalex.us_tools import SETTINGS


class MontyAlexException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)

class MontyAppException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)

class MontySettingsException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class TyperException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)

class TyperAppException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class CacheException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class ConsoleException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class DirectoryException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class FileSystemException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class TimeException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class UserOptionsException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class UserSettingsException(BaseException):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.message} {self.value}'

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


USER_TIMEZONE = SETTINGS.get_value('default.info.timezone')

class TrackFile:
    def __init__(self, file_path: bool) -> None:
        self.file_path: str = file_path
        self.file_exists: bool = pathexists(file_path)
        self.created_at: str = get_mtax_time()
        self.updated_at: str = None

    def __bool__(self) -> bool:
        return self.file_exists

    def __str__(self) -> str:
        return self.file_path

    def __repr__(self) -> str:
        if self.updated_at:
            return f'File(updated_at={self.updated_at!r})'
        return f'File(created_at={self.created_at!r})'

    def updated(self) -> bool:
        return bool(self.updated_at)

    def update(self):
        self.updated_at = get_mtax_time()

def get_mtax_time():
    if USER_TIMEZONE and USER_TIMEZONE != 'Notfound':
        timemod = MtaxTime(USER_TIMEZONE)
    else:
        print('No timezone found in settings, using default GMT')
        timemod = MtaxTime()
    return timemod.timestamp()

def mkfile(dirname: str, filename: str, global_: bool = False):
    directory: str = None
    if global_:
        directory = joinpaths(expanduser('~'), dirname)
    else:
        directory = joinpaths(curr_workdir, dirname)
    if not pathexists(directory):
        print('Directory does not exist')
        cancel()
    file_path = joinpaths(directory, filename)
    track: TrackFile = TrackFile(file_path)

    print(track)
    print(repr(track))
    print(bool(track))

def rmfile_(path: Any):
    rmfile(path)  #  No effect for now, potentially a rework at a later stage

def mktree():
    """Should consist of mkdirs and mkfile loops 
    to create a single file, list of files, or set of files
    (A set meaning unique "lists" for each unique directory made)"""
