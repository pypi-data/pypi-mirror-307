import deepcompare


def test_compare_str_with_str():
    # test full equality
    assert deepcompare.compare("abc", "abc")

    # test non-equality
    assert not deepcompare.compare("abc", "a")
    assert not deepcompare.compare("abc", "ab")
    assert not deepcompare.compare("abc", "abcd")


def test_compare_str_in_list_with_str_in_list():
    # test full equality
    assert deepcompare.compare(["a", "b", "c"], ["a", "b", "c"])

    # test partial equality
    assert not deepcompare.compare(["a", "b", "c"], ["a"])
    assert not deepcompare.compare(["a", "b", "c"], ["a", "b"])
    assert not deepcompare.compare(["a", "b", "c"], ["a", "c"])

    # test non-equality
    assert not deepcompare.compare(["a", "b", "c"], ["c", "b", "a"])
    assert not deepcompare.compare(["a", "b", "c"], ["a", "c", "b"])
    assert not deepcompare.compare(["a", "b", "c"], ["a", "b", "c", "d"])


def test_compare_list_with_list():
    # test full equality
    assert deepcompare.compare([1, 2, 3], [1, 2, 3])

    # test partial equality
    assert not deepcompare.compare([1, 2, 3], [1])
    assert not deepcompare.compare([1, 2, 3], [1, 2])
    assert not deepcompare.compare([1, 2, 3], [1, 3])

    # test non-equality
    assert not deepcompare.compare([1, 2, 3], [3, 2, 1])
    assert not deepcompare.compare([1, 2, 3], [2, 3, 1])
    assert not deepcompare.compare([1, 2, 3], [1, 2, 3, 4])


def test_compare_tuple_with_tuple():
    # test full equality
    assert deepcompare.compare((1, 2, 3), (1, 2, 3))

    # test partial equality
    assert not deepcompare.compare((1, 2, 3), (1,))
    assert not deepcompare.compare((1, 2, 3), (1, 2))
    assert not deepcompare.compare((1, 2, 3), (1, 3))

    # test non-equality
    assert not deepcompare.compare((1, 2, 3), (3, 2, 1))
    assert not deepcompare.compare((1, 2, 3), (2, 3, 1))
    assert not deepcompare.compare((1, 2, 3), (1, 2, 3, 4))


def test_compare_dict_with_dict():
    # test full equality
    assert deepcompare.compare({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3})

    # test partial equality
    assert not deepcompare.compare({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2})

    # test non-equality
    assert not deepcompare.compare(
        {"a": 1, "b": 2, "c": 3},
        {"a": 1, "b": 2, "c": 3, "d": 4},
    )


def test_compare_list_with_tuple_non_strict():
    # test full equality
    assert deepcompare.compare([1, 2, 3], (1, 2, 3))

    # test partial equality
    assert not deepcompare.compare([1, 2, 3], (1,))
    assert not deepcompare.compare([1, 2, 3], (1, 2))
    assert not deepcompare.compare([1, 2, 3], (1, 3))

    # test non-equality
    assert not deepcompare.compare([1, 2, 3], (3, 2, 1))
    assert not deepcompare.compare([1, 2, 3], (2, 3, 1))
    assert not deepcompare.compare([1, 2, 3], (1, 2, 3, 4))


def test_compare_list_with_tuple_strict():
    # test full equality with type mismatch
    assert not deepcompare.compare([1, 2, 3], (1, 2, 3), strict=True)

    # test partial equality with type mismatch
    assert not deepcompare.compare([1, 2, 3], (1,), strict=True)
    assert not deepcompare.compare([1, 2, 3], (1, 2), strict=True)
    assert not deepcompare.compare([1, 2, 3], (1, 3), strict=True)

    # test non-equality with type mismatch
    assert not deepcompare.compare([1, 2, 3], (3, 2, 1), strict=True)
    assert not deepcompare.compare([1, 2, 3], (2, 3, 1), strict=True)
    assert not deepcompare.compare([1, 2, 3], (1, 2, 3, 4), strict=True)


def test_compare_tuple_with_list_non_strict():
    # test full equality
    assert deepcompare.compare((1, 2, 3), [1, 2, 3])

    # test partial equality
    assert not deepcompare.compare((1, 2, 3), [1])
    assert not deepcompare.compare((1, 2, 3), [1, 2])
    assert not deepcompare.compare((1, 2, 3), [1, 3])

    # test non-equality
    assert not deepcompare.compare((1, 2, 3), [3, 2, 1])
    assert not deepcompare.compare((1, 2, 3), [2, 3, 1])
    assert not deepcompare.compare((1, 2, 3), [1, 2, 3, 4])


def test_compare_tuple_with_list_strict():
    # test full equality with type mismatch
    assert not deepcompare.compare((1, 2, 3), [1, 2, 3], strict=True)

    # test partial equality with type mismatch
    assert not deepcompare.compare((1, 2, 3), [1], strict=True)
    assert not deepcompare.compare((1, 2, 3), [1, 2], strict=True)
    assert not deepcompare.compare((1, 2, 3), [1, 3], strict=True)

    # test non-equality with type mismatch
    assert not deepcompare.compare((1, 2, 3), [3, 2, 1], strict=True)
    assert not deepcompare.compare((1, 2, 3), [2, 3, 1], strict=True)
    assert not deepcompare.compare((1, 2, 3), [1, 2, 3, 4], strict=True)


def test_compare_list_with_dict_non_strict():
    # test non-equality
    assert not deepcompare.compare([1, 2, 3], {"a": 1, "b": 2, "c": 3})
    assert not deepcompare.compare([1, 2, 3], {"a": 1, "b": 2})
    assert not deepcompare.compare([1, 2, 3], {"a": 1, "b": 2, "c": 3, "d": 4})


def test_compare_list_with_dict_strict():
    # test non-equality with type mismatch
    assert not deepcompare.compare([1, 2, 3], {"a": 1, "b": 2, "c": 3}, strict=True)
    assert not deepcompare.compare([1, 2, 3], {"a": 1, "b": 2}, strict=True)
    assert not deepcompare.compare(
        [1, 2, 3],
        {"a": 1, "b": 2, "c": 3, "d": 4},
        strict=True,
    )


def test_compare_tuple_with_dict_non_strict():
    # test non-equality
    assert not deepcompare.compare((1, 2, 3), {"a": 1, "b": 2, "c": 3})
    assert not deepcompare.compare((1, 2, 3), {"a": 1, "b": 2})
    assert not deepcompare.compare((1, 2, 3), {"a": 1, "b": 2, "c": 3, "d": 4})


def test_compare_tuple_with_dict_strict():
    # test non-equality with type mismatch
    assert not deepcompare.compare((1, 2, 3), {"a": 1, "b": 2, "c": 3}, strict=True)
    assert not deepcompare.compare((1, 2, 3), {"a": 1, "b": 2}, strict=True)
    assert not deepcompare.compare(
        (1, 2, 3),
        {"a": 1, "b": 2, "c": 3, "d": 4},
        strict=True,
    )


def test_compare_with_none_non_strict():
    # test full equality
    assert deepcompare.compare(None, None)

    # test non-equality
    assert not deepcompare.compare(None, [1, 2, 3])
    assert not deepcompare.compare(None, (1, 2, 3))
    assert not deepcompare.compare(None, {"a": 1, "b": 2, "c": 3})


def test_compare_with_none_strict():
    # test full equality
    assert deepcompare.compare(None, None, strict=True)

    # test non-equality
    assert not deepcompare.compare(None, [1, 2, 3], strict=True)
    assert not deepcompare.compare(None, (1, 2, 3), strict=True)
    assert not deepcompare.compare(None, {"a": 1, "b": 2, "c": 3}, strict=True)
