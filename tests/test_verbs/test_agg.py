import itertools as it

from clumper import Clumper

import pytest


def test_no_group_simple_agg(base_clumper):
    """
    Ensure that we can count the number of items.
    """
    c = base_clumper.agg(n=("i", "count")).collect()
    assert c[0]["n"] == 26


def test_no_group_multi_agg(base_clumper):
    """
    Ensure that we can count the number of items.
    """
    c = base_clumper.agg(
        n=("i", "count"), i_min=("i", "min"), i_max=("i", "max")
    ).collect()
    assert c[0]["n"] == 26
    assert c[0]["i_min"] == 0
    assert c[0]["i_max"] == 25


@pytest.mark.parametrize("n", [1, 5, 10])
def test_with_groups(n):
    """
    We should never count more rows than we have in the original data.
    """
    prod = it.product(range(1, n + 1), [-0.1, 0.0, 0.1], [True, False], ["a", "b"])
    clump = Clumper([{"r": 1, "i": i, "j": j, "a": a, "b": b} for i, j, a, b in prod])
    length = len(clump)
    n_items = clump.group_by("a", "b").agg(r=("r", "sum")).sum("r")
    assert n_items == length
