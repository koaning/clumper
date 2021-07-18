from clumper import Clumper
import pytest


@pytest.fixture(scope="module")
def base_clumper():
    """A standard clumper object that tests can use"""
    data = [
        {"data": [i for _ in range(2)], "i": i, "c": c}
        for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")
    ]
    return Clumper(data)
