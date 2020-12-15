import pytest

from clumper import Clumper


@pytest.mark.parametrize("keyname", ["foo", "bar", "buz"])
def test_can_rename_key(keyname):
    """We should be able to change the keyname"""
    data = {
        "f1": {"p1": 1, "p2": 2},
        "f2": {"p1": 3, "p2": 4},
        "f3": {"p1": 5, "p2": 6},
    }

    expected = [
        {"p1": 1, "p2": 2, keyname: "f1"},
        {"p1": 3, "p2": 4, keyname: "f2"},
        {"p1": 5, "p2": 6, keyname: "f3"},
    ]

    assert (
        Clumper(data, listify=False).flatten_keys(keyname=keyname).collect() == expected
    )


def test_len_appropriate_dict_input():
    """You can pass a dictionary, but then the length should be 1. Not the number of keys."""
    assert len(Clumper({"a": 1, "b": 2, "c": 3})) == 1
