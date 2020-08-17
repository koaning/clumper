import pytest
import os
from clumper import Clumper


def test_local_write_exists(tmp_path):
    """Test that an error is raised if the written file JSONL doesn't exists."""
    path = str(tmp_path / "cards_copy.jsonl")
    clump = Clumper.read_jsonl("tests/data/cards.jsonl")
    clump.write_jsonl(path)
    assert os.path.exists(path)


def test_local_read_write_content_same(tmp_path):
    """Test that an error is raised if the written JSONL file is not the same as what is read locally"""
    path = str(tmp_path / "cards_copy.jsonl")
    writer = Clumper.read_jsonl("tests/data/cards.jsonl")
    writer.write_jsonl(path)
    reader = Clumper.read_jsonl(path)
    assert reader.collect() == writer.collect()


def test_cloud_read_write_content_same(tmp_path):
    """Test that an error is raised if the written JSONL file is not the same as what is read from the cloud"""
    path = str(tmp_path / "pokemon_copy.jsonl")
    writer = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl")
    writer.write_jsonl(path)
    reader = Clumper.read_jsonl(path)
    assert reader.collect() == writer.collect()


@pytest.mark.parametrize("lines, expected", [(None, 4), (1, 1), (2, 2), (5, 4)])
def test_local_read_write_same_lines(tmp_path, lines, expected):
    """Test that an error is raised if the locally written files has the same number of lines as expected"""
    path = str(tmp_path / "cards_copy.jsonl")
    writer = Clumper.read_jsonl("tests/data/cards.jsonl", lines)
    writer.write_jsonl(path)
    reader = Clumper.read_jsonl(path)
    assert len(reader) == len(writer)
