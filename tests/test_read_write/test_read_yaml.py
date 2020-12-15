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


def test_big_file_explodes_properly():
    c = Clumper.read_yaml("tests/data/test-case-big.yaml").explode("videos")
    print(c.collect())
    assert False
    assert len(c) == 8
