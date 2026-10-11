from clumper import Clumper


def test_group_by_two_columns_with_missing_combination():
    """agg() over two columns must not mix up group keys when one combination is missing (issue #99)."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "a", "grp_2": "c", "value": 30},
        {"grp_1": "b", "grp_2": "a", "value": 40},
        {"grp_1": "b", "grp_2": "b", "value": 50},
    ]

    result = (
        Clumper(data).group_by("grp_1", "grp_2").agg(total=("value", "sum")).collect()
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
    """agg() over two columns keeps group keys correct when several combinations are missing."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "c", "value": 20},
        {"grp_1": "b", "grp_2": "b", "value": 30},
        {"grp_1": "c", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data).group_by("grp_1", "grp_2").agg(total=("value", "sum")).collect()
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
    """agg() over three columns keeps group keys correct when a combination is missing."""
    data = [
        {"a": "x", "b": "p", "c": "1", "value": 10},
        {"a": "x", "b": "p", "c": "2", "value": 20},
        {"a": "x", "b": "q", "c": "1", "value": 30},
        {"a": "y", "b": "p", "c": "1", "value": 40},
    ]

    result = Clumper(data).group_by("a", "b", "c").agg(total=("value", "sum")).collect()

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
    """agg() over two columns still works when every combination is present."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "b", "grp_2": "a", "value": 30},
        {"grp_1": "b", "grp_2": "b", "value": 40},
    ]

    result = (
        Clumper(data).group_by("grp_1", "grp_2").agg(total=("value", "sum")).collect()
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
    """transform() over two grouping columns returns the right value on every row."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "b", "value": 20},
        {"grp_1": "b", "grp_2": "a", "value": 30},
        {"grp_1": "b", "grp_2": "b", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .transform(double=("value", lambda x: [v * 2 for v in x]))
        .collect()
    )

    assert all(row["double"] == [row["value"] * 2] for row in result)


def test_group_by_two_columns_mutate():
    """mutate() over two grouping columns computes the right value on every row."""
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
    """sort() over two grouping columns keeps every row."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 30},
        {"grp_1": "a", "grp_2": "b", "value": 10},
        {"grp_1": "b", "grp_2": "a", "value": 40},
        {"grp_1": "b", "grp_2": "b", "value": 20},
    ]

    result = (
        Clumper(data).group_by("grp_1", "grp_2").sort(lambda d: d["value"]).collect()
    )

    assert len(result) == len(data)


def test_group_by_four_columns_with_missing_combination():
    """agg() over four columns keeps group keys correct when combinations are missing."""
    data = [
        {"a": 1, "b": 1, "c": 1, "d": 1, "value": 10},
        {"a": 1, "b": 1, "c": 1, "d": 2, "value": 20},
        {"a": 1, "b": 1, "c": 2, "d": 1, "value": 30},
        {"a": 2, "b": 1, "c": 1, "d": 1, "value": 40},
    ]

    result = (
        Clumper(data).group_by("a", "b", "c", "d").agg(total=("value", sum)).collect()
    )

    totals = {(row["a"], row["b"], row["c"], row["d"]): row["total"] for row in result}

    assert totals[(1, 1, 1, 1)] == 10
    assert totals[(1, 1, 1, 2)] == 20
    assert totals[(1, 1, 2, 1)] == 30
    assert totals[(2, 1, 1, 1)] == 40


def test_group_by_two_columns_with_multiple_aggregations():
    """agg() with several aggregations at once pairs every result with the right group."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "a", "value": 20},
        {"grp_1": "a", "grp_2": "b", "value": 30},
        {"grp_1": "b", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .agg(
            total=("value", sum),
            count=("value", len),
        )
        .collect()
    )

    results = {
        (row["grp_1"], row["grp_2"]): (row["total"], row["count"]) for row in result
    }

    assert results[("a", "a")] == (30, 2)
    assert results[("a", "b")] == (30, 1)
    assert results[("b", "a")] == (40, 1)


def test_group_by_two_columns_transform_multiple_missing_combinations():
    """transform() still works when several two-column combinations are missing."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "c", "value": 20},
        {"grp_1": "b", "grp_2": "b", "value": 30},
        {"grp_1": "c", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .transform(total=("value", "sum"))
        .collect()
    )

    assert len(result) == len(data)
    for row in result:
        assert row["total"] == row["value"]


def test_group_by_three_columns_transform_with_missing_combination():
    """transform() still works over three columns when a combination is missing."""
    data = [
        {"a": "x", "b": "p", "c": "1", "value": 10},
        {"a": "x", "b": "p", "c": "2", "value": 20},
        {"a": "x", "b": "q", "c": "1", "value": 30},
        {"a": "y", "b": "p", "c": "1", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("a", "b", "c")
        .transform(total=("value", "sum"))
        .collect()
    )

    assert len(result) == len(data)
    for row in result:
        assert row["total"] == row["value"]


def test_group_by_two_columns_mutate_multiple_missing_combinations():
    """mutate() still works when several two-column combinations are missing."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "c", "value": 20},
        {"grp_1": "b", "grp_2": "b", "value": 30},
        {"grp_1": "c", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .mutate(doubled=lambda d: d["value"] * 2)
        .collect()
    )

    assert len(result) == len(data)
    by_key = {(d["grp_1"], d["grp_2"]): d for d in data}
    for row in result:
        original = by_key[(row["grp_1"], row["grp_2"])]
        assert row["doubled"] == original["value"] * 2


def test_group_by_three_columns_mutate_with_missing_combination():
    """mutate() still works over three columns when a combination is missing."""
    data = [
        {"a": "x", "b": "p", "c": "1", "value": 10},
        {"a": "x", "b": "p", "c": "2", "value": 20},
        {"a": "x", "b": "q", "c": "1", "value": 30},
        {"a": "y", "b": "p", "c": "1", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("a", "b", "c")
        .mutate(doubled=lambda d: d["value"] * 2)
        .collect()
    )

    assert len(result) == len(data)
    by_key = {(d["a"], d["b"], d["c"]): d for d in data}
    for row in result:
        original = by_key[(row["a"], row["b"], row["c"])]
        assert row["doubled"] == original["value"] * 2


def test_group_by_two_columns_sort_multiple_missing_combinations():
    """sort() still keeps every row when several two-column combinations are missing."""
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 30},
        {"grp_1": "a", "grp_2": "c", "value": 10},
        {"grp_1": "b", "grp_2": "b", "value": 20},
        {"grp_1": "c", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .sort(key=lambda d: d["value"])
        .collect()
    )

    assert len(result) == len(data)
    assert {(d["grp_1"], d["grp_2"], d["value"]) for d in result} == {
        (d["grp_1"], d["grp_2"], d["value"]) for d in data
    }


def test_group_by_three_columns_sort_with_missing_combination():
    """sort() still keeps every row over three columns when a combination is missing."""
    data = [
        {"a": "x", "b": "p", "c": "1", "value": 30},
        {"a": "x", "b": "p", "c": "2", "value": 10},
        {"a": "x", "b": "q", "c": "1", "value": 20},
        {"a": "y", "b": "p", "c": "1", "value": 40},
    ]

    result = (
        Clumper(data).group_by("a", "b", "c").sort(key=lambda d: d["value"]).collect()
    )

    assert len(result) == len(data)
    assert {(d["a"], d["b"], d["c"], d["value"]) for d in result} == {
        (d["a"], d["b"], d["c"], d["value"]) for d in data
    }
