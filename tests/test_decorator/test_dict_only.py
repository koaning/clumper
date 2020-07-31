import pytest

from clumper import Clumper


@pytest.fixture
def no_dict_clumper():
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
    with pytest.raises(ValueError):
        _ = getattr(no_dict_clumper, method)(no_dict_clumper)
