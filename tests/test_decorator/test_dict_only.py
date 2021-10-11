import pytest

from clumper import Clumper


@pytest.fixture
def no_dict_clumper():
    """Returns clumper based on numbers, not a dict"""
    return Clumper([1, 2, 3, 4])


@pytest.mark.parametrize(
    "method",
    [
        "agg",
        "transform",
        "_subsets",
        "select",
        "drop",
        "keys",
        "explode",
        "sum",
        "mean",
        "unique",
        "n_unique",
    ],
)
def test_error_raised(no_dict_clumper, method):
    """Ensure error is raised when a method requires a clumper of dictionaries"""
    with pytest.raises(ValueError):
        _ = getattr(no_dict_clumper, method)(no_dict_clumper)
