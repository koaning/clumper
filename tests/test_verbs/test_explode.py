import itertools as it

import pytest

from clumper import Clumper


def test_explode_basic(base_clumper):
    """
    Base clumper has a nested list of size two on each item.
    When we explode that, our new clumper should be twice as big.
    """
    assert len(base_clumper.explode(d="data")) == 2 * len(base_clumper)


@pytest.mark.parametrize("n,k", it.product([1, 5, 10], [1, 2, 3]))
def test_explode_many(n, k):
    """
    Ensure we do cartesian product elegantly with one nested set.
    """
    data = [{"i": i, "nested": [j for j in range(k)]} for i in range(n)]
    c = Clumper(data).explode(j="nested").count("j")
    assert c == n * k


@pytest.mark.parametrize("n,k", it.product([1, 5, 10], [1, 2, 3]))
def test_explode_many_many(n, k):
    """
    Ensure we do cartesian product elegantly with two nested sets.
    """
    data = [
        {"i": i, "n1": [j for j in range(k)], "n2": [j for j in range(k)]}
        for i in range(n)
    ]
    c = Clumper(data).explode(j="n1", k="n2").count("j")
    assert c == n * k * k


def test_correct_keys_kept():
    """
    Make sure that we keep the correct names of the keys.
    """
    data = [{"a": 1, "b": 1, "items": [1, 2]}, {"a": 2, "b": 1, "items": [3, 4]}]
    assert set(Clumper(data).explode("items").keys()) == {"items", "a", "b"}
    assert set(Clumper(data).explode("items", foobar="items").keys()) == {
        "items",
        "a",
        "b",
        "foobar",
    }
    assert set(Clumper(data).explode(items="items").keys()) == {"items", "a", "b"}
    assert set(Clumper(data).explode(item="items").keys()) == {"item", "a", "b"}
    assert set(Clumper(data).explode(a="items").keys()) == {"a", "b"}


def test_big_file_explodes_properly():
    c = Clumper.read_yaml("tests/data/test-case-big.yaml").explode("videos")
    assert len(c) == 8
