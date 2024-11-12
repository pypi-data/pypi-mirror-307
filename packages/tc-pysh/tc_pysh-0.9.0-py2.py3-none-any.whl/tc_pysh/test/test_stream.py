from tc_pysh.stream import Stream


def test_pass_through():
    s = Stream(range(1, 10))

    assert list(s) == list(range(1, 10))


def test_map_pass_through():
    s = Stream(range(1, 10)).map(lambda e: e)

    assert list(s) == list(range(1, 10))


def test_map_square():
    s = Stream(range(1, 10)).map(lambda e: e * e)

    assert list(s) == list(map(lambda e: e * e, range(1, 10)))


def test_last():
    s = Stream(range(1, 10))

    assert s.last() == 9


def test_first():
    s = Stream(range(1, 10))

    assert s.first() == 1


def test_sort():
    s = Stream([8, 7, 6, 5, 4, 3]).sort()

    assert list(s) == [3, 4, 5, 6, 7, 8]


def test_state():
    s = Stream(range(3))

    assert next(s) == 0
    assert next(s) == 1
    assert next(s) == 2


def test_filter_pass_through():
    s = Stream(range(10)).filter(lambda e: True)

    assert list(s) == list(range(10))


def test_filter_drop_all():
    s = Stream(range(10)).filter(lambda e: False)

    assert list(s) == []


def test_filter_event():
    s = Stream(range(10)).filter(lambda e: e % 2 == 0)

    assert list(s) == list(range(0, 10, 2))


def test_tail():
    s = Stream(range(10)).tail(3)

    assert list(s) == [7, 8, 9]


def test_enumerate():
    s = Stream(range(10)).enumerate()

    assert list(s) == list(zip(range(10), range(10)))
