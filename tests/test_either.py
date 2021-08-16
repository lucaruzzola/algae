from pyfunds.either import Right, Left


def test_map_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value
    f = lambda x: x + 1
    # WHEN: the function f is applied to the either through map
    result = r.map(f)
    # THEN: the result is Right and contains the correct value
    assert result._is_right() and result._value == f(initial_value)


def test_map_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    l = Left(initial_value)
    # AND: a function that acts on the value
    f = lambda x: x + 1
    # WHEN: the function f is applied to the either through map
    result = l.map(f)
    # THEN: the result is Left and contains the initial value
    assert result._is_left() and result._value == initial_value


def test_flatmap_right_to_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value, returning a Right
    f = lambda x: Right(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Right and contains the correct value
    assert result._is_right() and result._value == f(initial_value)._value


def test_flatmap_right_to_left():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value, returning a Left
    f = lambda x: Left(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Left and contains the correct value
    assert result._is_left() and result._value == f(initial_value)._value


def test_flatmap_left_to_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    r = Left(initial_value)
    # AND: a function that acts on the value
    f = lambda x: Right(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Left and contains the initial value
    assert result._is_left() and result._value == initial_value


def test_swap_to_left():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # WHEN: we swap Left and Right
    swapped = r.swap()
    # THEN: the swapped result is Left and contains the initial value
    assert swapped._is_left() and swapped._value == initial_value


def test_swap_to_right():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    r = Left(initial_value)
    # WHEN: we swap Left and Right
    swapped = r.swap()
    # THEN: the swapped result is Right and contains the initial value
    assert swapped._is_right() and swapped._value == initial_value


def test_fold_from_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value when Either is Right
    fr = lambda x: x + 1
    # AND: a function that acts on the value when Either is Left
    fl = lambda x: 0
    # WHEN: the functions fl and fr are applied to the either through fold
    result = r.fold(fl, fr)
    # THEN: the result is the correct value and the correct function has been called
    assert result == fr(initial_value)


def test_fold_from_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    r = Left(initial_value)
    # AND: a function that acts on the value when Either is Right
    fr = lambda x: x + 1
    # AND: a function that acts on the value when Either is Left
    fl = lambda x: 0
    # WHEN: the functions fl and fr are applied to the either through fold
    result = r.fold(fl, fr)
    # THEN: the result is the correct value and the correct function has been called
    assert result == fl(initial_value)
