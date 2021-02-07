import pathlib
import pytest
from clumper import Clumper


@pytest.mark.parametrize("lines, expected", [(None, 800), (1, 1), (2, 2), (801, 800)])
def test_local_read_json_expected(lines, expected):
    """The number of lines read is not equal to expected number of lines"""
    clump = Clumper.read_json(pathlib.Path("tests/data/pokemon.json"), lines)
    assert len(clump) == expected
    clump = Clumper.read_json("tests/data/pokemon.json", lines)
    assert len(clump) == expected


def test_raise_error_n_zero():
    with pytest.raises(ValueError):
        Clumper.read_json("tests/data/pokemon.json", n=0)
