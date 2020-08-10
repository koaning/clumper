import pytest
import os
from clumper import Clumper


@pytest.mark.datafiles("./tests/test_read_write/sample_jsonl_files/cards.jsonl")
def test_read_jsonl_all_lines(datafiles):
    path = str(datafiles)  # Convert from py.path object to path (str)

    file_path = str(os.path.join(path, "cards.jsonl"))
    assert os.path.isfile(file_path)  # Make sure its a file
    assert (
        len(Clumper.read_jsonl(file_path)) == 4
    )  # There are 4 rows in the sample file


@pytest.mark.datafiles("./tests/test_read_write/sample_jsonl_files/cards.jsonl")
def test_read_jsonl_limited_lines(datafiles):
    path = str(datafiles)  # Convert from py.path object to path (str)

    file_path = str(os.path.join(path, "cards.jsonl"))
    assert os.path.isfile(file_path)  # Make sure its a file
    assert len(Clumper.read_jsonl(file_path, lines=2)) == 2
