from clumper import Clumper
import pytest


@pytest.fixture(scope="module")
def base_clumper():
    data = [
        {"data": [i for _ in range(2)], "i": i, "c": c}
        for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")
    ]
    return Clumper(data)


@pytest.fixture(scope="module")
def single_local_jsonl_file_path():
    return "tests/cards.jsonl"


@pytest.fixture(scope="module")
def single_cloud_jsonl_file_path():
    return "https://calmcode.io/datasets/pokemon.jsonl"

