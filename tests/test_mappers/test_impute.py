from clumper import Clumper
from clumper.sequence import impute


def test_correct_values_prev():
    """Check that we can impute by taking the previous value."""
    list_dicts = [
        {"a": 1, "b": 2},
        {"a": 2, "b": 3},
        {"a": 3},
        {"a": 4, "b": 6},
        {"a": 5},
    ]

    res = Clumper(list_dicts).mutate(b=impute("b", strategy="prev")).collect()

    assert [d["b"] for d in res] == [2, 3, 3, 6, 6]


def test_correct_values_value():
    """Check that we can impute by filling in a base value."""
    list_dicts = [
        {"a": 1, "b": 2},
        {"a": 2, "b": 3},
        {"a": 3},
        {"a": 4, "b": 6},
        {"a": 5},
    ]

    res = (
        Clumper(list_dicts)
        .mutate(b=impute("b", strategy="value", fallback=0))
        .collect()
    )

    assert [d["b"] for d in res] == [2, 3, 0, 6, 0]
