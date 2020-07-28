import pytest

from clumper import Clumper


@pytest.mark.parametrize("n", [1, 5, 10])
def test_n_unique1(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "n_unique")).collect()[0]["s"] == n


@pytest.mark.parametrize("n", [1, 5, 10])
def test_n_unique2(n):
    c = Clumper([{"i": 1} for i in range(1, n + 1)])
    assert c.agg(s=("i", "n_unique")).collect()[0]["s"] == 1


@pytest.mark.parametrize("n", [0, 1, 5, 10])
def test_count(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "count")).collect()[0]["s"] == n


@pytest.mark.parametrize("n", [1, 5, 10])
def test_sum1(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "sum")).collect()[0]["s"] == n * (n + 1) / 2


@pytest.mark.parametrize("n", [1, 5, 10])
def test_sum2(n):
    c = Clumper([{"i": 1} for i in range(1, n + 1)])
    assert c.agg(s=("i", "sum")).collect()[0]["s"] == n


@pytest.mark.parametrize("n", [1, 5, 10])
def test_mean1(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "mean")).collect()[0]["s"] == n * (n + 1) / 2 / n


@pytest.mark.parametrize("n", [1, 5, 10])
def test_mean2(n):
    c = Clumper([{"i": 1} for i in range(1, n + 1)])
    assert c.agg(s=("i", "mean")).collect()[0]["s"] == 1


@pytest.mark.parametrize("n", [1, 5, 10])
def test_unique(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert len(c.agg(s=("i", "unique")).collect()[0]["s"]) == n


@pytest.mark.parametrize("n", [1, 5, 10])
def test_minimum(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "min")).collect()[0]["s"] == 1


@pytest.mark.parametrize("n", [1, 5, 10])
def test_maximum(n):
    c = Clumper([{"i": i} for i in range(1, n + 1)])
    assert c.agg(s=("i", "max")).collect()[0]["s"] == n
