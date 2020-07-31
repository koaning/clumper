import json
import pathlib

import pytest

from clumper import Clumper


@pytest.fixture()
def pokemon():
    return json.loads(pathlib.Path("tests/pokemon.json").read_text())


def test_no_mutate_query(pokemon):
    """
    This was an error that happened in the past.
    """
    r1 = (
        Clumper(pokemon)
        .keep(lambda d: len(d["type"]) == 2)
        .mutate(type=lambda d: d["type"][0])
    )

    r2 = (
        Clumper(pokemon)
        .keep(lambda d: len(d["type"]) == 2)
        .mutate(type=lambda d: d["type"][0])
    )

    assert len(r1) == len(r2)


def test_not_all_combinations_matter():
    data = [
        {"a": 1, "b": 1, "items": [1, 2], "values": [3, 4]},
        {"a": 2, "b": 2, "items": [3, 2], "values": [5]},
    ]

    clumper = Clumper(data).explode(item="items", val="values")

    _ = (
        clumper.group_by("a", "b")
        .transform(item=("item", "unique"), values=("val", "unique"))
        .collect()
    )
