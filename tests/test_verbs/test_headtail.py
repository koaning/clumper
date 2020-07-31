import pytest


@pytest.mark.parametrize("n,expected", [(0, 0), (5, 5), (10, 10), (26, 26), (1000, 26)])
def test_headtail_size(base_clumper, n, expected):
    """
    If we grab 1000 elements out of a set of 26, we should just grab 26. No errors.
    """
    assert len(base_clumper.head(n)) == expected
    assert len(base_clumper.tail(n)) == expected


@pytest.mark.parametrize("idx", [i for i in range(1, 26)])
def test_can_collect_head(base_clumper, idx):
    """
    When we pick the first n=10 from the set of 26 then the last element
    should be 9 because we start counting at one. Repeat for n=1..26.
    """
    collected = base_clumper.head(idx).collect()
    assert collected[-1]["i"] == idx - 1


@pytest.mark.parametrize("idx", [i for i in range(1, 26)])
def test_can_collect_tail(base_clumper, idx):
    """
    When we pick the last n=10 from the set of 26 then
    the first element should be 26 - 10 = 16. Repeat for n=1..26.
    """
    collected = base_clumper.tail(idx).collect()
    assert collected[0]["i"] == 26 - idx


@pytest.mark.parametrize("n", [-1, 2.5, "a"])
def test_errors_raises(base_clumper, n):
    """
    Ensure that we raise errors when bad values of `n` go in.
    """
    with pytest.raises(ValueError):
        base_clumper.head(n)
    with pytest.raises(ValueError):
        base_clumper.tail(n)
