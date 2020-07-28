from clumper import Clumper


def test_length_list():
    """
    Basic tests to ensure that len() works as expected.
    """
    assert len(Clumper([])) == 0
    assert len(Clumper([{"a": 1}])) == 1
    assert len(Clumper([{"a": 1} for i in range(100)])) == 100


def test_mutability_insurance():
    """
    We don't want to change the original data going in. Ever.
    """
    data = [{"a": 1}, {"b": 2}]
    blob = Clumper(data).blob
    assert id(data) != id(blob)
