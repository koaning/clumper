from clumper import Clumper


def test_case_zero():
    """We need to raise sensible defaults on an empty clumper"""
    empty_c = Clumper([])
    assert empty_c.mean("i") is None
    assert empty_c.max("i") is None
    assert empty_c.min("i") is None
    assert empty_c.sum("i") is None
    assert empty_c.unique("i") == []
    assert empty_c.n_unique("i") == 0
