import pathlib
import pytest
from clumper import Clumper


@pytest.mark.parametrize("lines, expected", [(None, 800), (1, 1), (2, 2), (801, 800)])
def test_local_read_json_expected(lines, expected):
    """The number of lines read is not equal to expected number of lines"""
    clump = Clumper.read_json(pathlib.Path("tests/data/pokemon.json"), n=lines)
    assert len(clump) == expected
    clump = Clumper.read_json("tests/data/pokemon.json", n=lines)
    assert len(clump) == expected


def test_read_filepath():
    data = Clumper.read_json("tests/data/pokemon.json", add_path=True).collect()
    assert all([d["read_path"] == "tests/data/pokemon.json" for d in data])


def test_raise_error_n_zero():
    with pytest.raises(ValueError):
        Clumper.read_json("tests/data/pokemon.json", n=0)
