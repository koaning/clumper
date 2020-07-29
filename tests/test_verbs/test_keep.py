import pytest
from clumper import Clumper


def test_can_collect_all(base_clumper):
    """
    Confirm extreme value cases.
    """
    assert len(base_clumper.keep(lambda d: True)) == len(base_clumper)
    assert len(base_clumper.keep(lambda d: False)) == 0


@pytest.mark.parametrize("elem", "qwertyuiopasdfghjklzxcvbnm")
def test_can_pluck_single_element(base_clumper, elem):
    """
    We can pluck single elements by selecting on the character.
    """
    collected = base_clumper.keep(lambda d: d["c"] == elem).collect()
    assert collected[0]["c"] == elem
    assert len(collected) == 1


@pytest.mark.parametrize("start,end", [(0, 10), (10, 20), (20, 26)])
def test_can_collect_none(base_clumper, start, end):
    """
    We can select subsets by starting/ending at certain values for `i`.
    Let's check if the lengths match up.
    """
    c = base_clumper.keep(lambda d: (start <= d["i"]) & (d["i"] < end))
    assert len(c) == end - start


def test_keep_does_not_mutate():
    """
    The original data must not be changed. This happened originally.
    """
    data = [{"a": 1}, {"a": 2}]
    c = Clumper(data).keep(lambda d: d["a"] == 1)
    assert len(data) == 2
    assert len(c) == 1


def test_keep_multiple_queries(base_clumper):
    c = base_clumper.keep(lambda d: d["i"] < 20, lambda d: d["i"] >= 10)
    assert len(c) == 10
