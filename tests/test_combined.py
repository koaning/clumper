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
