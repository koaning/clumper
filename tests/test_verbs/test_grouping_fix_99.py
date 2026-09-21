from clumper import Clumper


def test_group_by_two_columns_with_missing_combination():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "a", "grp_2": "c", "value": 30},
        {"grp_1": "b", "grp_2": "a", "value": 40},
        {"grp_1": "b", "grp_2": "b", "value": 50},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .agg(total=("value", "sum"))
        .collect()
    )

    expected = [
        {"grp_1": "a", "grp_2": "a", "total": 10},
        {"grp_1": "a", "grp_2": "b", "total": 20},
        {"grp_1": "a", "grp_2": "c", "total": 30},
        {"grp_1": "b", "grp_2": "a", "total": 40},
        {"grp_1": "b", "grp_2": "b", "total": 50},
    ]

    assert sorted(result, key=lambda x: (x["grp_1"], x["grp_2"])) == sorted(
        expected, key=lambda x: (x["grp_1"], x["grp_2"])
    )


def test_group_by_two_columns_with_multiple_missing_combinations():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "c", "value": 20},
        {"grp_1": "b", "grp_2": "b", "value": 30},
        {"grp_1": "c", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .agg(total=("value", "sum"))
        .collect()
    )

    expected = [
        {"grp_1": "a", "grp_2": "a", "total": 10},
        {"grp_1": "a", "grp_2": "c", "total": 20},
        {"grp_1": "b", "grp_2": "b", "total": 30},
        {"grp_1": "c", "grp_2": "a", "total": 40},
    ]

    assert sorted(result, key=lambda x: (x["grp_1"], x["grp_2"])) == sorted(
        expected, key=lambda x: (x["grp_1"], x["grp_2"])
    )


def test_group_by_three_columns_with_missing_combination():
    data = [
        {"a": "x", "b": "p", "c": "1", "value": 10},
        {"a": "x", "b": "p", "c": "2", "value": 20},
        {"a": "x", "b": "q", "c": "1", "value": 30},
        {"a": "y", "b": "p", "c": "1", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("a", "b", "c")
        .agg(total=("value", "sum"))
        .collect()
    )

    expected = [
        {"a": "x", "b": "p", "c": "1", "total": 10},
        {"a": "x", "b": "p", "c": "2", "total": 20},
        {"a": "x", "b": "q", "c": "1", "total": 30},
        {"a": "y", "b": "p", "c": "1", "total": 40},
    ]

    assert sorted(result, key=lambda x: (x["a"], x["b"], x["c"])) == sorted(
        expected, key=lambda x: (x["a"], x["b"], x["c"])
    )


def test_group_by_two_columns_with_all_combinations_present():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "b", "grp_2": "a", "value": 30},
        {"grp_1": "b", "grp_2": "b", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .agg(total=("value", "sum"))
        .collect()
    )

    expected = [
        {"grp_1": "a", "grp_2": "a", "total": 10},
        {"grp_1": "a", "grp_2": "b", "total": 20},
        {"grp_1": "b", "grp_2": "a", "total": 30},
        {"grp_1": "b", "grp_2": "b", "total": 40},
    ]

    assert sorted(result, key=lambda x: (x["grp_1"], x["grp_2"])) == sorted(
        expected, key=lambda x: (x["grp_1"], x["grp_2"])
    )

def test_group_by_two_columns_transform():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "b", "grp_2": "a", "value": 30},
        {"grp_1": "b", "grp_2": "b", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .transform(
             double=("value", lambda x:[v * 2 for v in x])
        )
        .collect()
    )

    assert all(row["double"] == [row["value"] * 2] for row in result)


def test_group_by_two_columns_mutate():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "b", "grp_2": "a", "value": 30},
        {"grp_1": "b", "grp_2": "b", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .mutate(double=lambda d: d["value"] * 2)
        .collect()
    )

    assert all(row["double"] == row["value"] * 2 for row in result)


def test_group_by_two_columns_sort():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 30},
        {"grp_1": "a", "grp_2": "b", "value": 10},
        {"grp_1": "b", "grp_2": "a", "value": 40},
        {"grp_1": "b", "grp_2": "b", "value": 20},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .sort(lambda d: d["value"])
        .collect()
    )

    assert len(result) == len(data)
 