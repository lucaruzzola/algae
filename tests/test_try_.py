import math

import pytest

from algae.either import Left, Right
from algae.option import Nothing, Some
from algae.try_ import Failure, Success, Try


def unsafe_f(value: int):
    return math.log(value)


def test_apply_success():
    # GIVEN: an unsafe function that might raise an Exception for some input values
    # WHEN: the invocation of the function with a input value that doesn't raise an Exception is wrapped by Try.apply
    # THEN: the result is Success and contains the result of applying the function to the input value
    assert Try.apply(unsafe_f, 1) == Success(0)


def test_apply_failure():
    # GIVEN: an unsafe function that might raise an Exception for some input values
    # WHEN: the invocation of the function with a input value that raises an Exception is wrapped by Try.apply
    # THEN: the result is Failure and contains the raised Exception
    assert Try.apply(unsafe_f, 0) == Failure(ValueError("math domain error"))


def test_get_success():
    # GIVEN: an initial value
    value = 42
    # AND: a Success that contains the value
    success = Success(value)
    # WHEN: the .get method is called on the Success
    # THEN: the result is the initial value
    assert success.get() == value


def test_get_failure():
    # GIVEN: an Exception
    exc = Exception("")
    # AND: a Failure that contains the Exception
    fail = Failure(exc)
    # WHEN: the .get method is called on the Failure
    # THEN: the initial Exception is raised
    with pytest.raises(Exception):
        fail.get()


def test_get_or_else_success():
    # GIVEN: a value
    value = 42
    # AND: a default value
    default_value = 84
    # AND: a Success containing the value
    success = Success(value)
    # WHEN: the .get_or_else method is called on the Success
    # THEN: it returns the initial value
    assert success.get_or_else(default_value) == value


def test_get_or_else_failure():
    # GIVEN: a value
    value = 42
    # AND: a default value
    default_value = 84
    # AND: a Failure containing the Exception with the value as its text
    exc = Exception(value)
    # WHEN: the .get_or_else method is called on the Failure
    # THEN: it returns the default value
    fail = Failure(exc)
    assert fail.get_or_else(default_value) == default_value


def test_map_success():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND: a function returning the other value for any input
    f = lambda x: other_value
    # AND: a Success containing the initial value
    success = Success(value)
    # WHEN: .map is called on the Success
    # THEN: it returns a Success containing the result of calling the provided function on the content of the Success
    assert success.map(f) == Success(other_value)


def test_map_failure():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND: a function returning the other value
    f = lambda x: other_value
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: .map is called on the Failure
    # THEN: it returns the Failure
    assert fail.map(f) == Failure(exc)


def test_flat_map_success_to_success():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND: a function returning a Success that contains the other value
    f = lambda x: Success(other_value)
    # AND: a Success containing the value
    success = Success(value)
    # WHEN: .flat_map is called on the Success
    # THEN: it returns the result of applying f to the content of the Success
    assert success.flat_map(f) == Success(other_value)


def test_flat_map_success_to_failure():
    # GIVEN: a value
    value = 42
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # AND: a function returning the Failure
    f = lambda x: fail
    # AND: a Success
    success = Success(value)
    # WHEN: .flat_map is called on the Success
    # THEN: it returns the result of applying f to the content of the Success
    assert success.flat_map(f) == Failure(exc)


def test_flat_map_failure_to_failure():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND: a function returning a Success
    f = lambda x: Success(other_value)
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: .flat_map is called on the Failure
    # THEN: it returns the Failure without applying f
    assert fail.flat_map(f) == Failure(exc)


def test_fold_from_success():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND a failure string
    fail_str = "failure"
    # AND: one function to deal with the Success case
    fs = lambda x: other_value
    # AND: one function to deal with the Failure case
    ff = lambda x: fail_str
    # AND: a Success
    success = Success(value)
    # WHEN: .fold is called on the Success
    # THEN: the result of applying fs is returned
    assert success.fold(ff, fs) == other_value


def test_fold_from_failure():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND a failure string
    fail_str = "failure"
    # AND: one function to deal with the Success case
    fs = lambda x: other_value
    # AND: one function to deal with the Failure case
    ff = lambda x: fail_str
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: .fold is called on the Failure
    # THEN: the result of applying ff is returned
    assert fail.fold(ff, fs) == fail_str


def test_to_either_success():
    # GIVEN: a value
    value = 42
    # AND: a Success containing the value
    success = Success(value)
    # WHEN: .to_either is called on the Success
    # THEN: the result is a Right containing the value
    assert success.to_either() == Right(value)


def test_to_either_failure():
    # GIVEN: a value
    value = 42
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: .to_either is called on the Failure
    # THEN: the result is a Left containing the value
    assert fail.to_either() == Left(exc)


def test_to_option_success():
    # GIVEN: a value
    value = 42
    # AND: a Success containing the value
    success = Success(value)
    # WHEN: .to_option is called on the Success
    # THEN: the result is a Some containing the value
    assert success.to_option() == Some(value)


def test_to_option_failure():
    # GIVEN: a value
    value = 42
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: .to_option is called on the Failure
    # THEN: the result is Nothing
    assert fail.to_option() == Nothing()


def test_equals_success():
    # GIVEN: a value
    value = 42
    # AND: a Success containing the value
    success = Success(42)
    # WHEN: two instances of Success containing the same value are compared
    # THEN: the result is True
    assert Success(value) == success and success == Success(value)


def test_equals_failure():
    # GIVEN: a value
    value = 42
    # AND: a Failure containing an Exception with the value as its text
    exc = Exception(value)
    fail = Failure(exc)
    # WHEN: two instances of Nothing
    # THEN: the result is True
    assert Failure(exc) == fail and fail == Failure(exc)


def test_not_equals():
    # GIVEN: a value
    value = 42
    # AND: another value
    other_value = 84
    # AND: a Success containing the value
    success = Success(value)
    # AND: a Success containing the other value
    other_success = Success(other_value)
    # AND: a Failure containing an Exception
    exc = Exception(value)
    fail = Failure(exc)
    # AND: a Failure containing another Exception
    other_exc = Exception(other_value)
    other_fail = Failure(other_exc)
    # WHEN: they are compared with each other
    # THEN: they all return False
    assert (
        success != fail
        and fail != success
        and other_success != success
        and success != other_success
        and other_fail != fail
        and fail != other_fail
    )
