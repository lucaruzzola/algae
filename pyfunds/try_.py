from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Callable, TypeVar, Union, Generic, Any, Dict, List

T = TypeVar("T")
U = TypeVar("U")


class Try(ABC, Generic[T]):
    def __init__(self):
        super().__init__()

    @staticmethod
    def apply(f: Callable[[Any], T], *args: List[Any], **kwargs: Dict[str, Any]) -> Try[T]:
        try:
            return Success(f(*args, **kwargs))
        except Exception as e:
            return Failure(e)

    @abstractmethod
    def _is_failure(self) -> bool:
        pass

    def _is_success(self) -> bool:
        return not self._is_failure()

    @abstractmethod
    def get(self) -> Union[T, Exception]:
        pass

    @abstractmethod
    def get_or_else(self, default: T) -> T:
        pass

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Try[U]:
        pass

    @abstractmethod
    def flat_map(self, f: Callable[[T], Try[U]]) -> Try[U]:
        pass

    @abstractmethod
    def fold(self, ff: Callable[[Exception], U], fs: Callable[[T], U]) -> U:
        pass


class Success(Try):
    def __init__(self, value: T):
        super().__init__()
        self._value = value


    def _is_failure(self) -> bool:
        return False

    def get(self) -> Union[T, Exception]:
        return self._value

    def get_or_else(self, default: T) -> T:
        return self.get()

    def map(self, f: Callable[[T], U]) -> Try[U]:
        return Try.apply(f, self.get())

    def flat_map(self, f: Callable[[T], Try[U]]) -> Try[U]:
        return f(self._value)

    def fold(self, ff: Callable[[Exception], U], fs: Callable[[T], U]) -> U:
        try:
            return fs(self.get())
        except Exception as e:
            return ff(e)


class Failure(Try):
    def __init__(self, exception: Exception):
        super().__init__()
        self._exception = exception

    def _is_failure(self) -> bool:
        return True

    def get(self) -> Union[T, Exception]:
        raise self._exception

    def get_or_else(self, default: T) -> T:
        return default

    def map(self, f: Callable[[T], U]) -> Try[U]:
        return self

    def flat_map(self, f: Callable[[T], Try[U]]) -> Try[U]:
        return self

    def fold(self, ff: Callable[[Exception], U], fs: Callable[[T], U]) -> U:
        return ff(self._exception)