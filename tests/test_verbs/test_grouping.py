def test_mutate_does_not_remove_groups(base_clumper):
    """Ensure we don't remove groups via mutate"""
    grps = base_clumper.group_by("i").mutate(i2=lambda d: d["i"] * 2).groups
    assert grps == ("i",)


def test_sort_does_not_remove_groups(base_clumper):
    """Ensure we don't remove groups via sort"""
    grps = base_clumper.group_by("i").sort(lambda d: d["i"]).groups
    assert grps == ("i",)
