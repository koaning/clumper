from clumper import Clumper


def test_can_collect_all():
    data = [{"i": i} for i in range(10)]
    c = Clumper(data)
    assert len(c.keep(lambda d: d["i"] < 20).collect()) == 10


def test_can_collect_half():
    data = [{"i": i} for i in range(10)]
    c = Clumper(data)
    assert len(c.keep(lambda d: d["i"] < 5).collect()) == 5


def test_can_collect_none():
    data = [{"i": i} for i in range(10)]
    c = Clumper(data)
    assert len(c.keep(lambda d: d["i"] < 0).collect()) == 0
