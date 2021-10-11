from clumper import Clumper


def test_correct_keys():
    """
    Ensure that the original key of the dictionary is replaced with the new one.
    """
    data = [
        {"a": 1, "b": 1, "item": 1},
        {"a": 1, "b": 1, "item": 2},
        {"a": 1, "b": 1, "item": 1},
        {"a": 2, "b": 2, "c": 2, "item": 3},
        {"a": 2, "b": 2, "c": 2, "item": 2},
    ]

    keys = Clumper(data).group_by("a", "b").implode(items="item").keys()
    assert set(keys) == {"a", "b", "c", "items"}
