from algae.either import Left, Right


def test_map_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value
    f = lambda x: x + 1
    # WHEN: the function f is applied to the either through map
    result = r.map(f)
    # THEN: the result is Right and contains the correct value
    assert result == Right(f(initial_value))


def test_map_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    l = Left(initial_value)
    # AND: a function that acts on the value
    f = lambda x: x + 1
    # WHEN: the function f is applied to the either through map
    result = l.map(f)
    # THEN: the result is Left and contains the initial value
    assert result == Left(initial_value)


def test_flatmap_right_to_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value, returning a Right
    f = lambda x: Right(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Right and contains the correct value
    assert result == f(initial_value)


def test_flatmap_right_to_left():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # AND: a function that acts on the value, returning a Left
    f = lambda x: Left(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Left and contains the correct value
    assert result == f(initial_value)


def test_flatmap_left_to_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    r = Left(initial_value)
    # AND: a function that acts on the value
    f = lambda x: Right(x + 1)
    # WHEN: the function f is applied to the either through flatmap
    result = r.flat_map(f)
    # THEN: the result is Left and contains the initial value
    assert result == Left(initial_value)


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


def test_swap_to_left():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # WHEN: it's swapped
    swapped = r.swap()
    # THEN: the swapped result is Left and contains the initial value
    assert swapped == Left(initial_value)


def test_swap_to_right():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    r = Left(initial_value)
    # WHEN: it's swapped
    swapped = r.swap()
    # THEN: the swapped result is Right and contains the initial value
    assert swapped == Right(initial_value)


def test_equals_right():
    # GIVEN: an instance of Either that is Right with an initial value
    initial_value = 5
    r = Right(initial_value)
    # WHEN: equality between two instances or Right with the same value is checked
    # THEN: the equality holds both ways
    assert r == Right(initial_value) and Right(initial_value) == r


def test_equals_left():
    # GIVEN: an instance of Either that is Left with an initial value
    initial_value = 5
    l = Left(initial_value)
    # WHEN: equality between two instances or Left with the same value is checked
    # THEN: the equality holds both ways
    assert l == Left(initial_value) and Left(initial_value) == l


def test_not_equals():
    # GIVEN: different instances of Left and Right, with 2 possible values
    initial_value = 5
    other_value = 10
    r = Right(initial_value)
    r2 = Right(other_value)
    l = Left(initial_value)
    l2 = Left(other_value)
    # WHEN: they are compared for equality
    # THEN: none of the equalities holds
    assert (
        r != r2
        and r2 != r
        and r != l
        and l != r
        and r != l2
        and l2 != r
        and l != l2
        and l2 != l
    )
