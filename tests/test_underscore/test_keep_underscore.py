import pytest


from clumper import Clumper
from clumper.underscore import _


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_underscore_simple_mutate(n):
    c = Clumper([{"a": i} for i in range(20)])
    res1 = c.keep(lambda d: d["a"] % n == 0)
    res2 = c.keep(f"_['a'] % {n} == 0")
    res3 = c.keep(_["a"] % n == 0)
    assert res1.equals(res2)
    assert res2.equals(res3)
