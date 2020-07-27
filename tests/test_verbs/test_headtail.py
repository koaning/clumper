from clumper import Clumper


def test_headtail_size(base_clumper):
    assert len(base_clumper.head(10)) == 10
    assert len(base_clumper.tail(10)) == 10
    assert len(base_clumper.head(5)) == 5
    assert len(base_clumper.tail(5)) == 5


def test_can_collect_tail():
    data = [{"i": i} for i in range(10)]
    c = Clumper(data).tail(1)
    collected = c.collect()
    assert collected[0]["i"] == 9


def test_can_collect_head():
    data = [{"i": i} for i in range(10)]
    c = Clumper(data).head(1)
    collected = c.collect()
    assert collected[0]["i"] == 0
