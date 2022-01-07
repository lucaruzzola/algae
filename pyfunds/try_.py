from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar, Union

from pyfunds.either import Either, Left, Right
from pyfunds.option import Nothing, Option, Some

T = TypeVar("T")
U = TypeVar("U")


class Try(ABC, Generic[T]):
    def __init__(self):
        super().__init__()

    @staticmethod
    def apply(f: Callable[[Any], T], *args: Any, **kwargs: Any) -> Try[T]:
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

    @abstractmethod
    def to_either(self) -> Either[Exception, T]:
        pass

    @abstractmethod
    def to_option(self) -> Option[T]:
        pass

    def __str__(self) -> str:
        return f"Try is {'Success' if self._is_success() else 'Failure'}"

    def __repr__(self) -> str:
        return "pyfunds.Try"

    @abstractmethod
    def __eq__(self, other: Try[T]) -> bool:
        pass

    def __ne__(self, other: Try[T]) -> bool:
        return not self == other


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
        return f(self.get())

    def fold(self, ff: Callable[[Exception], U], fs: Callable[[T], U]) -> U:
        try:
            return fs(self.get())
        except Exception as e:
            return ff(e)

    def to_either(self) -> Either[Exception, T]:
        return Right(self.get())

    def to_option(self) -> Option[T]:
        return Some(self.get())

    def __str__(self) -> str:
        return f"Try is Success with value: {self._value.__repr__()} of type {type(self._value)}"

    def __repr__(self) -> str:
        return f"pyfunds.Succes({self._value.__repr__()})"

    def __eq__(self, other: Try[T]) -> bool:
        if other._is_failure():
            return False
        else:
            return self.get() == other.get()


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

    def to_either(self) -> Either[Exception, T]:
        return Left(self._exception)

    def to_option(self) -> Option[T]:
        return Nothing()

    def __str__(self) -> str:
        return f"Try is Failure with exception type: {type(self._exception)} and args {self._exception.args}"

    def __repr__(self) -> str:
        return f"pyfunds.Failure({self._exception.__repr__()})"

    def __eq__(self, other: Try[T]) -> bool:
        if other._is_success():
            return False
        else:
            return (
                type(self._exception) == type(other._exception)
                and self._exception.args == other._exception.args
            )
