import pytest

from algae.option import NoElement, Nothing, Option, Some


def test_apply_some():
    # GIVEN: a value that is not None
    value = "Blbsr"
    # WHEN: apply is used to create an instance of Option
    some = Option.apply(value)
    # THEN: the instance of Option is created as Some, is not empty or Nothing,
    # and is equal to Some(value)
    assert not some._is_empty() and some == Some(value) and some != Nothing()


def test_apply_nothing():
    # GIVEN: a value that is None
    value = None
    # WHEN: apply is used to create an instance of Option
    nothing = Option.apply(value)
    # THEN: the instance of Option is created as Nothing, and it's empty
    assert nothing._is_empty() and nothing == Nothing()


def test_get_some():
    # GIVEN: an instance of Some created with a value that is not None
    value = "Chrmndr"
    some = Some(value)
    # WHEN: the get method is used
    # THEN: it returns the initial value
    assert some.get() == value


def test_get_nothing():
    # GIVEN: an instance of Nothing
    nothing = Nothing()
    # WHEN: the get method is used
    # THEN: a NoElement exception is raised
    with pytest.raises(NoElement):
        nothing.get()


def test_get_or_else_some():
    value = "Pkch"
    some = Some(value)
    alternative = "Pk"
    assert some.get_or_else(alternative) == value


def test_get_or_else_nothing():
    nothing = Nothing()
    default_value = nothing.get_or_else("Pk")
    assert default_value == "Pk"


def test_when_some():
    # GIVEN: a instance of value that is not None
    value = "Sqrtl"
    # AND: a method that returns a boolean

    def is_monster(name: str) -> bool:
        return name in ("Blbsr", "Chrmndr", "Sqrtl", "Pkch")

    # WHEN: the 'when' method is used to create an instance of Option, and the boolean method returns True
    some = Option.when(is_monster(value), "pk")
    # THEN: the instance of Option is a Some of the value passed
    assert some == Some("pk")


def test_when_nothing():
    # GIVEN: a instance of value that is not None
    value = "Foo"
    # AND: a method that returns a boolean

    def is_monster(name: str):
        return name in ("Blbsr", "Chrmndr", "Sqrtl", "Pkch")

    # WHEN: the 'when' method is used to create an instance of Option, and the boolean method returns False
    nothing = Option.when(is_monster(value), "pk")
    # THEN: the instance of Option is Nothing
    assert nothing == Nothing()


def test_map_some():
    # GIVEN: an instance of Some that contains a value that is not None
    value = "Pk"
    some = Some(value)
    # AND: a method that acts on the value
    mod = "two"
    f = lambda x: x + mod
    # WHEN: the method is applied to the Option instance using map
    mapped_some = some.map(f)
    # THEN: the result is Some(f(value))
    assert mapped_some == Some(value + mod)


def test_map_nothing():
    # GIVEN: an instance of Nothing
    nothing = Nothing()
    # AND: a method that acts on the value
    mod = "two"
    f = lambda x: x + mod
    # WHEN: the method is applied to the Option instance using map
    mapped_nothing = nothing.map(f)
    # THEN: the result is Noting
    assert mapped_nothing == Nothing()


def test_flat_map_some_to_some():
    # GIVEN: an instance of Some that contains a value that is not None
    value = "Chrzrd"
    some = Some(value)
    # AND: a method that acts on the value and returns an Option
    statement = "is a monster"
    f = lambda x: Some(x + statement)
    # WHEN: the method is applied to the Option instance using flat_map
    flat_mapped_some = some.flat_map(f)
    # THEN: the result is f(value)
    assert flat_mapped_some == Some(value + statement)


def test_flat_map_some_to_nothing():
    # GIVEN: an instance of Some that contains a value that is not None
    value = "Chrzrd"
    some = Some(value)
    # AND: a method that acts on the value and returns Nothing
    f = lambda x: Nothing()
    # WHEN: the method is applied to the Option instance using flat_map
    flat_mapped_some = some.flat_map(f)
    # THEN: the result is Nothing
    assert flat_mapped_some == Nothing()


def test_flat_map_nothing_to_nothing():
    # GIVEN: an instance of Nothing
    nothing = Nothing()
    # AND: a method that acts on the value and returns an Option
    f = lambda x: Some("Chrzrd")
    # WHEN: the method is applied to the Option instance using flat_map
    flat_mapped_nothing = nothing.flat_map(f)
    # THEN: the result is Nothing
    assert flat_mapped_nothing == Nothing()


def fold_from_some():
    # GIVEN: an instance of Some that contains a value that is not None
    value = "Blsts"
    some = Some(value)
    # AND: a default value
    default_value = "Pkch"
    # AND: a method that acts on the value
    new_value = "Vnsr"
    f = lambda x: new_value
    # WHEN: the fold method is called on the Option with the default value and the method f
    folded_some = some.fold(default_value, f)
    # THEN: the result is f(value)
    assert folded_some == new_value


def fold_from_nothing():
    # GIVEN: an instance of Nothing
    some = Nothing()
    # AND: a default value
    default_value = "Pkch"
    # AND: a method that acts on the value
    new_value = "Vnsr"
    f = lambda x: new_value
    # WHEN: the fold method is called on the Option with the default value and the method f
    folded_some = some.fold(default_value, f)
    # THEN: the result is the default value
    assert folded_some == default_value


def test_equals_some():
    # GIVEN: an instance of Some with a value
    value = "Pkch"
    some = Some(value)
    # WHEN: it's compared to another Some with the same value
    # THEN: both are equal to the other
    assert some == Some(value) and Some(value) == some


def test_equals_nothing():
    # GIVEN: an instance of Nothing
    nothing = Nothing()
    # WHEN: it's compared to another Nothing
    # THEN: both are equal to the other
    assert nothing == Nothing() and Nothing() == nothing


def test_not_equals():
    # GIVEN: an instance of Some
    value = "Pkch"
    some = Some(value)
    # AND: another instance of Some with a different value
    other_value = "Pk"
    other_some = Some(other_value)
    # AND: an instance of Nothing
    nothing = Nothing()
    # WHEN: they are compared
    # THEN: none of them are equal to the others
    assert (
        some != other_some
        and other_some != some
        and some != nothing
        and nothing != some
        and other_some != nothing
        and nothing != other_some
    )
