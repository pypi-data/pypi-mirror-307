from json import JSONDecodeError
from montyalex.typing_tools import Any


class MontyBaseException(BaseException):
    def __init__(self, message: str, value: Any = None, name: str = 'MontyBaseException') -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}: {self.message} {self.value}'

    def __repr__(self) -> str:
        return self.name

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)

class MontyArithmeticException(ArithmeticError):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = 'MontyArithmeticException') -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}: {self.message} {self.value}'

    def __repr__(self) -> str:
        return self.name

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)

class MontyRangeError(MontyArithmeticException):
    def __init__(self, message: str, value: Any = None, name: str = 'RangeError') -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.value = value

class MontyKeyValueError(MontyBaseException): ...
class MontyJSONError(JSONDecodeError): ...
