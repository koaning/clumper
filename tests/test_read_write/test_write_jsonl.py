import pytest
import os
from clumper import Clumper


def test_local_write_exists(tmp_path):
    """Test that an error is raised if the written file JSONL doesn't exists."""
    path = str(tmp_path / "cards_copy.jsonl")
    clump = Clumper.read_jsonl("tests/data/cards.jsonl")
    clump.write_jsonl(path)
    assert os.path.exists(path)


@pytest.mark.parametrize("lines, expected", [(1, 1), (2, 2), (5, 4)])
def test_local_read_write_same_lines(tmp_path, lines, expected):
    """Test that the locally written files has the same number of lines as expected"""
    path = tmp_path / "cards_copy.jsonl"

    writer = Clumper.read_jsonl("tests/data/cards.jsonl", lines)
    writer.write_jsonl(path)

    reader = Clumper.read_jsonl(str(path))
    assert len(reader) == len(writer)
