import pytest
from mktestdocs import check_docstring, get_codeblock_members

from clumper import Clumper
from clumper.sequence import row_number, smoothing, expanding, rolling, impute


@pytest.mark.parametrize(
    "func",
    [row_number, smoothing, expanding, rolling, impute],
    ids=lambda d: d.__name__,
)
def test_docstring(func):
    """Check docstring of each function."""
    check_docstring(obj=func)


@pytest.mark.parametrize(
    "m", get_codeblock_members(Clumper), ids=lambda d: d.__qualname__
)
def test_clumper_docstrings(m):
    """
    Take the docstring of every method on the `Clumper` class.
    The test passes if the usage examples causes no errors.
    """
    check_docstring(m)
