from clumper import Clumper


def test_empty_list():
    assert len(Clumper([]).collect()) == 0
