import math

import pytest

from pyfunds.either import Left, Right
from pyfunds.option import Nothing, Some
from pyfunds.try_ import Failure, Success, Try


def unsafe_f(value: int):
    return math.log(value)


def test_apply_success():
    assert Try.apply(unsafe_f, 1) == Success(0)


def test_apply_failure():
    assert Try.apply(unsafe_f, 0) == Failure(ValueError("math domain error"))


def test_get_success():
    value = 42
    success = Success(value)
    assert success.get() == value


def test_get_failure():
    value = 42
    exc = Exception(value)
    fail = Failure(exc)
    with pytest.raises(Exception):
        fail.get()


def test_get_or_else_success():
    value = 42
    default_value = "fortytwo"
    success = Success(value)
    assert success.get_or_else(default_value) == value


def test_get_or_else_failure():
    value = 42
    default_value = "fortytwo"
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.get_or_else(default_value) == default_value


def test_map_success():
    value = 42
    other_value = "fortytwo"
    f = lambda x: other_value
    success = Success(value)
    assert success.map(f) == Success(other_value)


def test_map_failure():
    value = 42
    other_value = "fortytwo"
    f = lambda x: other_value
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.map(f) == Failure(exc)


def test_flat_map_success_to_success():
    value = 42
    other_value = "fortytwo"
    f = lambda x: Success(other_value)
    success = Success(value)
    assert success.flat_map(f) == Success(other_value)


def test_flat_map_success_to_failure():
    value = 42
    exc = Exception(value)
    fail = Failure(exc)
    f = lambda x: fail
    success = Success(value)
    assert success.flat_map(f) == Failure(exc)


def test_flat_map_failure_to_failure():
    value = 42
    other_value = "fortytwo"
    f = lambda x: Success(other_value)
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.flat_map(f) == Failure(exc)


def test_fold_from_success():
    value = 42
    other_value = "fortytwo"
    fail_str = "failure"
    fs = lambda x: other_value
    ff = lambda x: fail_str
    success = Success(value)
    assert success.fold(ff, fs) == other_value


def test_fold_from_failure():
    value = 42
    other_value = "fortytwo"
    fail_str = "failure"
    fs = lambda x: other_value
    ff = lambda x: fail_str
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.fold(ff, fs) == fail_str


def test_to_either_success():
    value = 42
    success = Success(value)
    assert success.to_either() == Right(value)


def test_to_either_failure():
    value = 42
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.to_either() == Left(exc)


def test_to_option_success():
    value = 42
    success = Success(value)
    assert success.to_option() == Some(value)


def test_to_option_failure():
    value = 42
    exc = Exception(value)
    fail = Failure(exc)
    assert fail.to_option() == Nothing()


def test_equals_success():
    value = 42
    success = Success(42)
    assert Success(value) == success and success == Success(value)


def test_equals_failure():
    value = 42
    exc = Exception(value)
    fail = Failure(exc)
    assert Failure(exc) == fail and fail == Failure(exc)


def test_not_equals():
    value = 42
    other_value = "fortytwo"
    success = Success(42)
    other_success = Success(other_value)
    exc = Exception(value)
    other_exc = Exception(other_value)
    fail = Failure(exc)
    other_fail = Failure(other_exc)
    assert (
        success != fail
        and fail != success
        and other_success != success
        and success != other_success
        and other_fail != fail
        and fail != other_fail
    )
