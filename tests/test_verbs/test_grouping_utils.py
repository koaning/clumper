import itertools as it

import pytest

from clumper import Clumper
from clumper.sequence import row_number


def test_group_combos_one_group():
    prod = it.product([1, 2, 3, 4, 5], [-0.1, 0.0, 0.1], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    res = clump.group_by("a")._group_combos()
    assert list(sorted(r["a"] for r in res)) == list(sorted([True, False]))
    res = clump.group_by("b")._group_combos()
    assert list(sorted(r["b"] for r in res)) == list(sorted(["a", "b"]))


def test_group_combos_two_groups():
    prod = it.product([1, 2, 3, 4, 5], [-0.1, 0.0, 0.1], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    assert len(clump.group_by("a", "b")._group_combos()) == 4


@pytest.mark.parametrize("keys,size", zip(["a", "b", "ab"], [8, 8, 4]))
def test_subsets_sizes(keys, size):
    prod = it.product([1, 2], [1, 2], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    for c in clump.group_by(*keys)._subsets():
        assert len(c) == size


def test_mutate_group_aware():
    """
    Does `row_number` reset during mutate if a group is active?
    """
    data = [{"bool": True if i % 2 else False} for i in range(20)]
    clump = Clumper(data).group_by("bool").mutate(r=row_number())
    assert len(clump) == len(data)
    assert clump.groups == ("bool",)
    assert set(clump.unique("r")) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
