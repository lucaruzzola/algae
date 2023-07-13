from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Union

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


class Either(ABC, Generic[L, R]):
    """ Represents a value of a coproduct. An instance of Either is an instance of either Left or Right.

    The implementation is right-biased, which means that Right is assumed to be the default case to operate on.
    If it is Left, operations like map() and flat_map() return the Left value unchanged.

    Right side of the Either. A swap() method is also provided, to cope with cases where map() needs to be called on the
    Left side.
    A common use case for Either is error handling, with some sort of error on the Left, and the wanted result on the
    Right, allowing for the composition of function to be short-circuited to return the error on the first Left returned
    and for the computation to continue otherwise.

    The left and right values are not meant to be accessed or overridden directly.
    """

    _value: Union[L, R]
    __match_args__ = "_value"
    __slots__ = "_value"

    def __init__(self, value: Union[L, R]):
        super().__init__()
        self._value = value

    def map(self, f: Callable[[R], T]) -> Either[L, T]:
        """
        Applies func to right side element if Either is a Right and wraps the return value in a Right,
               else it returns the Left Either.

        :param f: the function to be applied to the content of the Right side.
        :return: Right(func(right)) if either is right, left otherwise.
        """

        return Right(f(self._value)) if self._is_right() else self

    def flat_map(self, f: Callable[[R], Either[L, T]]) -> Either[L, T]:
        """
        Applies f to right side element if Either is Right, else it returns the Left Either.

        :param f: the function to be applied to the content of the Right side, returning a Right.
        :return: func(right) if either is right, left otherwise.
        """
        return f(self._value) if self._is_right() else self

    def fold(self, fl: Callable[[L], T], fr: Callable[[R], T]) -> T:
        """
        Applies fl to left if Either is Left, else applies fr to right, in both cases the return
        type of the passed functions is the same.

        :param fl: the function to be applied to the content of the Left side.
        :param fr: the function to be applied to the content of the Right side.
        :return: fl(left) if Either is Left, fr(right) if Either is Right.
        """

        return fr(self._value) if self._is_right() else fl(self._value)

    def swap(self) -> Either[R, L]:
        """
        Swap the Either, returning a Left if it was Right, and Right if it was Left.
        Useful to apply a function through map() or flat_map() to the left side is needed.

        :return: Left(right) if Either is right, Right(left) is Either is left.
        """
        return Left(self._value) if self._is_right() else Right(self._value)

    @abstractmethod
    def _is_right(self) -> bool:
        pass

    def _is_left(self) -> bool:
        return not self._is_right()

    def __str__(self) -> str:
        return f"Either is {'Right' if self._is_right() else 'Left'}, with value: {self._value.__repr__()} of type {type(self._value)}"

    def __repr__(self) -> str:
        return f"algae.Either({self._value.__repr__()})"

    def __eq__(self, other: Either[L, R]) -> bool:
        if self._is_left():
            return other._is_left() and self._value == other._value
        elif other._is_left():
            return False
        else:
            return self._value == other._value

    def __ne__(self, other: Either[L, R]) -> bool:
        return not self == other


class Right(Either):
    """
    The right side of the disjoint union, as opposed to the Left side.
    """
    def _is_right(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"algae.Right({self._value})"


class Left(Either):
    """
    The left side of the disjoint union, as opposed to the Right side.
    """
    def _is_right(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"algae.Left({self._value})"
