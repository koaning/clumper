import pytest
import os
from clumper import Clumper


@pytest.mark.parametrize("lines, expected", [(0, 0), (1, 1), (2, 2)])
def test_read_jsonl(single_json_file_name, lines, expected):

    assert os.path.isfile(single_json_file_name), "JSON file is not a file"
    assert (
        len(Clumper.read_jsonl(single_json_file_name, lines)) == expected
    ), "The number of lines read is not equal to expected number of lines"
