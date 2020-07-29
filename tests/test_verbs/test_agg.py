def test_no_group_simple_agg(base_clumper):
    """
    Ensure that we can count the number of items.
    """
    c = base_clumper.agg(n=("i", "count")).collect()
    assert c[0]["n"] == 26


def test_no_group_multi_agg(base_clumper):
    """
    Ensure that we can count the number of items.
    """
    c = base_clumper.agg(
        n=("i", "count"), i_min=("i", "min"), i_max=("i", "max")
    ).collect()
    assert c[0]["n"] == 26
    assert c[0]["i_min"] == 0
    assert c[0]["i_max"] == 25
