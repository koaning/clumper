import itertools as it

import pytest

from clumper import Clumper


def test_group_combos_one_group():
    prod = it.product([1, 2, 3, 4, 5], [-0.1, 0.0, 0.1], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    res = clump.group_by("a").group_combos()
    assert list(sorted(r["a"] for r in res)) == list(sorted([True, False]))
    res = clump.group_by("b").group_combos()
    assert list(sorted(r["b"] for r in res)) == list(sorted(["a", "b"]))


def test_group_combos_two_groups():
    prod = it.product([1, 2, 3, 4, 5], [-0.1, 0.0, 0.1], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    assert len(clump.group_by("a", "b").group_combos()) == 4


@pytest.mark.parametrize("keys,size", zip(["a", "b", "ab"], [8, 8, 4]))
def test_subsets_sizes(keys, size):
    prod = it.product([1, 2], [1, 2], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    for c in clump.group_by(*keys).subsets():
        assert len(c) == size
