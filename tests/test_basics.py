from clumper import Clumper


def test_length_list():
    """
    Basic tests to ensure that len() works as expected.
    """
    assert len(Clumper([])) == 0
    assert len(Clumper([{"a": 1}])) == 1
    assert len(Clumper([{"a": 1} for i in range(100)])) == 100
