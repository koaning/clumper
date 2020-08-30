import pytest
import os
from clumper import Clumper


def test_local_write_exists(tmp_path):
    """Test that an error is raised if the written file JSON doesn't exists."""
    path = str(tmp_path / "pokemon_copy.json")
    clump = Clumper.read_json("tests/data/pokemon.json")
    clump.write_json(path)
    assert os.path.exists(path)


@pytest.mark.parametrize("lines, expected", [(None, 4), (1, 1), (2, 2), (5, 4)])
def test_local_read_write_same_lines(tmp_path, lines, expected):
    """Test that an error is raised if the locally written files has the same number of lines as expected"""
    path = str(tmp_path / "pokemon_copy.json")
    writer = Clumper.read_json("tests/data/pokemon.json", lines)
    writer.write_json(path)
    reader = Clumper.read_json(path)
    assert len(reader) == len(writer)
