import pytest
from clumper import Clumper


@pytest.mark.parametrize("lines, expected", [(None, 4), (1, 1), (2, 2), (5, 4)])
def test_local_read_jsonl_expected(lines, expected):
    """The number of lines read is not equal to expected number of lines"""
    clump = Clumper.read_jsonl("tests/data/cards.jsonl", lines)
    assert len(clump) == expected


@pytest.mark.parametrize("lines, expected", [(None, 800), (1, 1), (2, 2), (801, 800)])
def test_cloud_read_jsonl_expected(lines, expected):
    """The number of lines read is not equal to expected number of lines"""
    clump = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl", lines)
    assert len(clump) == expected


def test_read_csv_negative_nrows():
    """Test that an error is raised if nrows is negative."""
    with pytest.raises(ValueError):
        Clumper.read_jsonl("tests/cards.jsonl", n=-5)


def test_read_csv_negative_zero():
    """Test that an error is raised if nrows is zero."""
    with pytest.raises(ValueError):
        Clumper.read_jsonl("tests/cards.jsonl", n=0)


def test_non_existing_file():
    with pytest.raises(FileNotFoundError):
        Clumper.read_jsonl("tests/cards.jsonl")
