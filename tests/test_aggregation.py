import pytest

from clumper import Clumper


def make_clumper(size, constant=False):
    return Clumper([{"i": 1 if constant else i} for i in range(size)])


@pytest.fixture(params=[1, 5, 10])
def n(request):
    return request.param


def test_case_zero():
    empty_c = Clumper([])
    assert empty_c.mean("i") is None
    assert empty_c.max("i") is None
    assert empty_c.min("i") is None
    assert empty_c.sum("i") is None
    assert empty_c.unique("i") == []
    assert empty_c.n_unique("i") == 0


def test_n_unique(n):
    assert make_clumper(n, constant=True).n_unique("i") == 1
    assert make_clumper(n, constant=False).n_unique("i") == n


def test_count(n):
    assert make_clumper(n, constant=False).count("i") == n
    assert make_clumper(n, constant=True).count("i") == n


def test_sum(n):
    assert make_clumper(n, constant=True).sum("i") == n
    assert make_clumper(n, constant=False).sum("i") == n * (n - 1) / 2


def test_mean(n):
    assert make_clumper(n, constant=True).mean("i") == 1
    assert make_clumper(n, constant=False).mean("i") == (n - 1) / 2


def test_unique(n):
    assert len(make_clumper(n, constant=False).unique("i")) == n


def test_minimum(n):
    assert make_clumper(n, constant=False).min("i") == 0


def test_maximum(n):
    assert make_clumper(n, constant=False).max("i") == n - 1
