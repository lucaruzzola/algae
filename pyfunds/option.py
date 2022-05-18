from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class NoElement(Exception):
    pass


class Option(ABC, Generic[T]):

    _value: T
    __match_args__ = "_value"
    __slots__ = "_value"

    def __init__(self):
        super().__init__()

    @staticmethod
    def apply(value: T):
        return Some(value) if value is not None else Nothing()

    @abstractmethod
    def _is_empty(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> T:
        pass

    def get_or_else(self, default: T) -> T:
        return default if self._is_empty() else self.get()

    @staticmethod
    def when(condition: bool, value: T) -> Option[T]:
        return Some(value) if condition else Nothing()

    def map(self, f: Callable[[T], U]) -> Option[U]:
        return Some(f(self.get())) if not self._is_empty() else self

    def flat_map(self, f: Callable[[T], Option[U]]) -> Option[U]:
        return f(self.get()) if not self._is_empty() else self

    def fold(self, default: U, fs: Callable[[T], U]) -> U:
        return default if self._is_empty() else fs(self.get())

    def __str__(self) -> str:

        return f"Option is {'Some' if not self._is_empty() else 'Nothing'}" + (
            f", containing value: {self.get().__repr__()} of type {type(self.get())}"
            if not self._is_empty()
            else ""
        )

    def __repr__(self) -> str:
        return "pyfunds.Option"

    def __eq__(self, other: Option[T]) -> bool:
        if self._is_empty():
            return other._is_empty()
        elif other._is_empty():
            return False
        else:
            return self.get() == other.get()

    def __ne__(self, other: Option[T]) -> bool:
        return not self == other


class Some(Option[T]):
    def __init__(self, value: T):
        super().__init__()
        self._value = value

    def _is_empty(self) -> bool:
        return False

    def get(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"pyfunds.Some({self.get()})"


class Nothing(Option[T]):
    def __init__(self):
        super().__init__()

    def _is_empty(self) -> bool:
        return True

    def get(self) -> T:
        raise NoElement

    def __repr__(self) -> str:
        return "pyfunds.Nothing"
