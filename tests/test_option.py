import pytest

from pyfunds.option import NoElement, Nothing, Option, Some


def test_equals_some():
    value = "Pikachu"
    some = Some(value)
    assert some == Some(value) and Some(value) == some


def test_equals_nothing():
    nothing = Nothing()
    assert nothing == Nothing() and Nothing() == nothing


def test_not_equals():
    value = "Pikachu"
    other_value = "Mew"
    nothing = Nothing()
    some = Some(value)
    assert (
        some != Some(other_value)
        and Some(other_value) != some
        and some != nothing
        and nothing != some
    )


def test_apply_some():
    some = Option.apply("Bulbasaur")
    assert not some._is_empty() and some == Some("Bulbasaur")


def test_apply_nothing():
    nothing = Option.apply(None)
    assert nothing._is_empty() and nothing == Nothing()


def test_get_some():
    value = "Charmander"
    some = Some(value)
    assert some.get() == value


def test_get_nothing():
    nothing = Nothing()
    with pytest.raises(NoElement):
        nothing.get()


def test_when_some():
    value = "Squirtle"

    def is_pokemon(name: str):
        return name in ("Bulbasaur", "Charmander", "Squirtle", "Pikachu")

    some = Option.when(is_pokemon(value), "pokemon")
    assert some == Some("pokemon")


def test_when_nothing():
    value = "Foo"

    def is_pokemon(name: str):
        return name in ("Bulbasaur", "Charmander", "Squirtle", "Pikachu")

    nothing = Option.when(is_pokemon(value), "pokemon")
    assert nothing == Nothing()


def test_get_or_else_some():
    value = "Pikachu"
    some = Some(value)
    alternative = "Mew"
    assert some.get_or_else(alternative) == value


def test_get_or_else_nothing():
    nothing = Nothing()
    default_value = nothing.get_or_else("Mew")
    assert default_value == "Mew"


def test_map_some():
    value = "Mew"
    some = Some(value)
    modification = "two"
    mapped_some = some.map(lambda x: x + modification)
    assert mapped_some == Some(value + modification)


def test_map_nothing():
    nothing = Nothing()
    mapped_nothing = nothing.map(lambda x: x + "two")
    assert mapped_nothing == Nothing()


def test_flat_map_some_to_some():
    value = "Charizard"
    some = Some(value)
    statement = "is a pokemon"
    flat_mapped_some = some.flat_map(lambda x: Some(x + statement))
    assert flat_mapped_some == Some(value + statement)


def test_flat_map_some_to_nothing():
    value = "Charizard"
    some = Some(value)
    flat_mapped_some = some.flat_map(lambda x: Nothing())
    assert flat_mapped_some == Nothing()


def test_flat_map_nothing_to_nothing():
    nothing = Nothing()
    flat_mapped_nothing = nothing.flat_map(lambda x: Some("Charizard"))
    assert flat_mapped_nothing == Nothing()


def fold_from_some():
    some = Some("Blastoise")
    default_value = "Pikachu"
    new_value = "Venusaur"
    folded_some = some.fold(default_value, lambda x: new_value)
    assert folded_some == new_value


def fold_from_nothing():
    some = Nothing()
    default_value = "Pikachu"
    new_value = "Venusaur"
    folded_some = some.fold(default_value, lambda x: new_value)
    assert folded_some == default_value
