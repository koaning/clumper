def test_can_overwrite(base_clumper):
    """
    Make sure that we can overwrite values.
    """
    new_clumper = base_clumper.mutate(i=lambda d: d["i"] * 2)
    zipped = zip(base_clumper.collect(), new_clumper.collect())
    assert all([c1["i"] * 2 == c2["i"] for c1, c2 in zipped])


def test_can_make_new(base_clumper):
    """
    Make sure that we create new values.
    """
    new_clumper = base_clumper.mutate(j=lambda d: d["i"] * 2)
    zipped = zip(base_clumper.collect(), new_clumper.collect())
    assert all([c1["i"] * 2 == c2["j"] for c1, c2 in zipped])


def test_can_reuse_call(base_clumper):
    """
    Make sure that we create new values using old values in
    the same call to mutate.
    """
    new_clumper = base_clumper.mutate(j=lambda d: d["i"] * 2, k=lambda d: d["j"] * 2)
    assert all([c["i"] * 2 == c["j"] for c in new_clumper.collect()])
    assert all([c["j"] * 2 == c["k"] for c in new_clumper.collect()])
