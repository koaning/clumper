import pathlib

import pytest

from clumper import Clumper


@pytest.mark.parametrize(
    "path,size",
    [
        ("tests/data/demo-flat-1.yaml", 3),
        ("tests/data/demo-flat-2.yaml", 3),
        ("tests/data/demo-nested.yml", 1),
    ],
)
def test_can_read_yaml_yml(path, size):
    """Test we can read in the basic files."""
    assert len(Clumper.read_yaml(path)) == size
    assert len(Clumper.read_yaml(pathlib.Path(path))) == size


@pytest.mark.parametrize("size,exp", [(10, 3), (3, 3), (2, 2), (1, 1)])
def test_can_read_lines(size, exp):
    """Test that we can determine the number of lines."""
    assert len(Clumper.read_yaml("tests/data/demo-flat-1.yaml", n=size)) == exp


@pytest.mark.parametrize(
    "url",
    [
        "http://calmcode.io/datasets/config-demo.yml",
        "https://calmcode.io/datasets/config-demo.yml",
    ],
)
def test_fetch_url(url):
    """Test that the url can be read both for http/https"""
    assert len(Clumper.read_yaml(url)) != 0


def test_multi_file_single_dict():
    """We should be able to read in files that contain only a single dict."""
    c = Clumper.read_yaml("tests/data/single-files/*.yml", listify=True)
    assert len(c) == 2
    assert len(c.explode("stuff")) == 6


def test_multi_file_single_dict_filepath():
    """We should be able to read in files that contain only a single dict and add a filepath."""
    c = Clumper.read_yaml("tests/data/single-files/*.yml", listify=True, add_path=True)
    paths = c.map(lambda d: d["read_path"]).collect()
    assert set(paths) == {
        "tests/data/single-files/single1.yml",
        "tests/data/single-files/single2.yml",
    }


def test_multi_file_single_file_filepath():
    """We should be able to read in non listified data with adding a path"""
    c = Clumper.read_yaml(
        "tests/data/single-files/single1.yml", listify=False, add_path=True
    ).collect()
    assert c["read_path"] == "tests/data/single-files/single1.yml"


def test_multi_file_add_path_many():
    """We check the path again, but now for data that is flat."""
    c = Clumper.read_yaml("tests/data/demo-flat-*.yaml", add_path=True)
    paths = c.map(lambda d: d["read_path"]).collect()
    assert set(paths) == {"tests/data/demo-flat-1.yaml", "tests/data/demo-flat-2.yaml"}
