import deepcompare


def test_compare_list_in_list_with_list_in_list():
    # test full equality
    assert deepcompare.partial_compare([[1, 2], 2, 3], [[1, 2], 2, 3])
    assert deepcompare.partial_compare([[1, 2], [2, 3], 3], [[1, 2], [2, 3], 3])
    assert deepcompare.partial_compare(
        [[1, 2], [2, 3], [3, 4]],
        [[1, 2], [2, 3], [3, 4]],
    )

    # test partial equality
    assert deepcompare.partial_compare([[1, 2], [2, 3], [3, 4]], [[1], [2, 3], [3, 4]])
    assert deepcompare.partial_compare([[1, 2], [2, 3], [3, 4]], [[1, 2], [2], [3, 4]])
    assert deepcompare.partial_compare([[1, 2], [2, 3], [3, 4]], [[1, 2], [2, 3], [3]])
    assert deepcompare.partial_compare([[1, 2], [2, 3], [3, 4]], [[1, 2], [2, 3]])

    # test non-equality
    assert not deepcompare.partial_compare([[1, 2], [2, 3], 3], [[1, 2], 2, 3])
    assert not deepcompare.partial_compare([[1, 2], [2, 3], [3, 4]], [[1, 2], 2, 3])


def test_compare_list_in_list_in_list_with_list_in_list_in_list():
    # test full equality
    assert deepcompare.partial_compare([[[1, 2], 2], 2, 3], [[[1, 2], 2], 2, 3])
    assert deepcompare.partial_compare(
        [[[1, 2], 2], [[2, 3], 3], 3],
        [[[1, 2], 2], [[2, 3], 3], 3],
    )

    # test partial equality
    assert deepcompare.partial_compare(
        [[[1, 2], 2], [[2, 3], 3], 3],
        [[[1], 2], [[2, 3], 3], 3],
    )
    assert deepcompare.partial_compare(
        [[[1, 2], 2], [[2, 3], 3], 3],
        [[[1, 2], 2], [[2], 3], 3],
    )
    assert deepcompare.partial_compare(
        [[[1, 2], 2], [[2, 3], 3], 3],
        [[[1, 2], 2], [[2, 3]], 3],
    )

    # test non-equality
    assert not deepcompare.partial_compare([[[1, 2], 2], 2, 3], [[1, 2], 2, 3])
    assert not deepcompare.partial_compare(
        [[[1, 2], 2], [[2, 3], 3], 3],
        [[[1, 2], 2], [2, 3], 3],
    )


def test_compare_tuple_in_list_with_tuple_in_list():
    # test full equality
    assert deepcompare.partial_compare([(1, 2), 2, 3], [(1, 2), 2, 3])
    assert deepcompare.partial_compare([(1, 2), (2, 3), 3], [(1, 2), [2, 3], 3])
    assert deepcompare.partial_compare(
        [(1, 2), (2, 3), (3, 4)],
        [(1, 2), (2, 3), (3, 4)],
    )

    # test partial equality
    assert deepcompare.partial_compare([(1, 2), (2, 3), (3, 4)], [(1,), (2, 3), (3, 4)])
    assert deepcompare.partial_compare([(1, 2), (2, 3), (3, 4)], [(1, 2), (2,), (3, 4)])
    assert deepcompare.partial_compare([(1, 2), (2, 3), (3, 4)], [(1, 2), (2, 3), (3,)])
    assert deepcompare.partial_compare([(1, 2), (2, 3), (3, 4)], [(1, 2), (2, 3)])

    # test non-equality
    assert not deepcompare.partial_compare([(1, 2), (2, 3), 3], [(1, 2), 2, 3])
    assert not deepcompare.partial_compare([(1, 2), (2, 3), (3, 4)], [(1, 2), 2, 3])


def test_compare_tuple_in_list_in_list_with_tuple_in_list_in_list():
    # test full equality
    assert deepcompare.partial_compare([[(1, 2), 2], 2, 3], [[(1, 2), 2], 2, 3])
    assert deepcompare.partial_compare(
        [[(1, 2), 2], [(2, 3), 3], 3],
        [[(1, 2), 2], [(2, 3), 3], 3],
    )

    # test partial equality
    assert deepcompare.partial_compare(
        [[(1, 2), 2], [(2, 3), 3], 3],
        [[(1,), 2], [(2, 3), 3], 3],
    )
    assert deepcompare.partial_compare(
        [[(1, 2), 2], [(2, 3), 3], 3],
        [[(1, 2), 2], [(2,), 3], 3],
    )
    assert deepcompare.partial_compare(
        [[(1, 2), 2], [(2, 3), 3], 3],
        [[(1, 2), 2], [(2, 3), 3]],
    )

    # test non-equality
    assert not deepcompare.partial_compare([[(1, 2), 2], 2, 3], [(1, 2), 2, 3])
    assert not deepcompare.partial_compare(
        [[(1, 2), 2], [(2, 3), 3], 3],
        [[(1, 2), 2], [2, 3], 3],
    )


def test_compare_dict_in_list_with_dict_in_list():
    # test full equality
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, 2, 3],
        [{"a": 1, "b": 2}, 2, 3],
    )
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, 3],
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, 3],
    )
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
    )

    # test partial equality
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
    )
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1, "b": 2}, {"c": 3}, {"e": 5, "f": 6}],
    )
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5}],
    )
    assert deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}],
    )

    # test non-equality
    assert not deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, 3],
        [{"a": 1, "b": 2}, 2, 3],
    )
    assert not deepcompare.partial_compare(
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5, "f": 6}],
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, 3],
    )


def test_compare_dict_in_list_in_list_with_dict_in_list_in_list():
    # test full equality
    assert deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], 2, 3],
        [[{"a": 1, "b": 2}, 2], 2, 3],
    )
    assert deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
    )

    # test partial equality
    assert deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
        [[{"a": 1}, 2], [{"c": 3, "d": 4}, 3], 3],
    )
    assert deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
        [[{"a": 1, "b": 2}, 2], [{"c": 3}, 3], 3],
    )
    assert deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3]],
    )

    # test non-equality
    assert not deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], 2, 3],
        [{"a": 1, "b": 2}, 2, 3],
    )
    assert not deepcompare.partial_compare(
        [[{"a": 1, "b": 2}, 2], [{"c": 3, "d": 4}, 3], 3],
        [[{"a": 1, "b": 2}, 2], [2, 3], 3],
    )


def test_compare_list_in_dict():
    # test full equality
    assert deepcompare.partial_compare({"a": [1, 2], "b": 3}, {"a": [1, 2], "b": 3})
    assert deepcompare.partial_compare(
        {"a": [1, 2], "b": [3, 4]},
        {"a": [1, 2], "b": [3, 4]},
    )

    # test partial equality
    assert deepcompare.partial_compare({"a": [1, 2], "b": 3}, {"a": [1, 2]})
    assert deepcompare.partial_compare(
        {"a": [1, 2], "b": [3, 4]},
        {"a": [1, 2], "b": [3]},
    )

    # test non-equality
    assert not deepcompare.partial_compare(
        {"a": [1, 2], "b": [3, 4]},
        {"a": [1, 2], "b": 3},
    )
    assert not deepcompare.partial_compare(
        {"a": [1, 2], "b": [3, 4]},
        {"a": [1, 2], "b": [3, 4, 5]},
    )
