import pytest

from clumper import Clumper


@pytest.mark.parametrize(
    "path,size", [("tests/data/demo-flat.yaml", 3), ("tests/data/demo-nested.yml", 1)]
)
def test_can_read_yaml_yml(path, size):
    """Test we can read in the basic files."""
    assert len(Clumper.read_yaml(path)) == size


@pytest.mark.parametrize("size,exp", [(10, 3), (3, 3), (2, 2), (1, 1)])
def test_can_read_lines(size, exp):
    """Test that we can determine the number of lines."""
    assert len(Clumper.read_yaml("tests/data/demo-flat.yaml", n=size)) == exp
