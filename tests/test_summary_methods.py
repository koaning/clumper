import pytest

from clumper import Clumper


def make_clumper(size, constant=False):
    """clumper generator function"""
    return Clumper([{"i": 1 if constant else i} for i in range(size)])


@pytest.fixture(params=[1, 5, 10])
def n(request):
    """number as a fixture"""
    return request.param


def test_n_unique(n):
    """Confirm that n_unique actually counts unique values"""
    assert make_clumper(n, constant=True).n_unique("i") == 1
    assert make_clumper(n, constant=False).n_unique("i") == n


def test_count(n):
    """Confirm that count actually counts values"""
    assert make_clumper(n, constant=False).count("i") == n
    assert make_clumper(n, constant=True).count("i") == n


def test_sum(n):
    """Confirm that count actually sums values"""
    assert make_clumper(n, constant=True).sum("i") == n
    assert make_clumper(n, constant=False).sum("i") == n * (n - 1) / 2


def test_mean(n):
    """Confirm that count actually takes the average of values"""
    assert make_clumper(n, constant=True).mean("i") == 1
    assert make_clumper(n, constant=False).mean("i") == (n - 1) / 2


def test_unique(n):
    """Confirm that count actually returns a sequence of unique values"""
    assert len(make_clumper(n, constant=False).unique("i")) == n


def test_minimum(n):
    """Confirm that count actually returns a minimum of values"""
    assert make_clumper(n, constant=False).min("i") == 0


def test_maximum(n):
    """Confirm that count actually returns a maximum of values"""
    assert make_clumper(n, constant=False).max("i") == n - 1
