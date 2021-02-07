import pathlib
import pytest
from itertools import product
from clumper import Clumper
from string import ascii_uppercase


paths = [
    "tests/data/monopoly.csv",
    "https://calmcode.io/datasets/monopoly.csv",
    pathlib.Path("tests/data/monopoly.csv"),
]
nrows = [(None, 22), (10, 10), (15, 15), [80, 22]]
fields = [
    (
        None,
        [
            "name",
            "rent",
            "house_1",
            "house_2",
            "house_3",
            "house_4",
            "hotel",
            "deed_cost",
            "house_cost",
            "color",
            "tile",
        ],
    ),
    (
        [
            "namee",
            "rent",
            "house1",
            "house2",
            "house3",
            "house4",
            "hotell",
            "deed_cost",
            "house_cost",
            "colour",
            "tille",
        ],
        [
            "namee",
            "rent",
            "house1",
            "house2",
            "house3",
            "house4",
            "hotell",
            "deed_cost",
            "house_cost",
            "colour",
            "tille",
        ],
    ),
]

path_nrows = [(path, nrows, length) for path, (nrows, length) in product(paths, nrows)]
path_fields = [
    (path, fieldnames, fields_check)
    for path, (fieldnames, fields_check) in product(paths, fields)
]


@pytest.mark.parametrize("path,nrows,length", path_nrows)
def test_read_csv(path, nrows, length):
    """Test that the length of clumper matches the total number of rows in the csv."""
    clump = Clumper.read_csv(path=path, n=nrows)
    assert len(clump) == length


@pytest.mark.parametrize("path,fieldnames,field_check", path_fields)
def test_fieldnames(path, fieldnames, field_check):
    """Test that fieldnames matches keys of Clumper."""
    clump = Clumper.read_csv(path=path, fieldnames=fieldnames)
    assert not set(field_check).difference(clump.keys())


def test_wrong_delimiter():
    """Test that an error is raised if a wrong delimiter is supplied."""
    with pytest.raises(TypeError):
        Clumper.read_csv("tests/data/monopoly.csv", delimiter=", ")


def test_read_csv_negative_nrows():
    """Test that an error is raised if nrows is negative."""
    with pytest.raises(ValueError):
        Clumper.read_csv("tests/data/monopoly.csv", n=-5)


def test_read_csv_negative_zero():
    """Test that an error is raised if nrows is zero."""
    with pytest.raises(ValueError):
        Clumper.read_csv("tests/data/monopoly.csv", n=0)


def test_read_csv_nulls():
    """Test that null rows are discarded."""
    assert Clumper.read_csv("tests/data/null.csv").equals(
        Clumper([{"a": "1", "b": "2"}, {"a": "2", "c": "4"}])
    )


def test_fieldnames_less_than():
    """Test number of keys returned when an incomplete number of fields is supplied."""
    reader = Clumper.read_csv("tests/data/monopoly.csv", fieldnames=["A", "B", "C"])
    assert set(reader.keys()) == {"A", "B", "C", None}
    assert len(reader.keys()) == len(["A", "B", "C"]) + 1


def test_fieldnames_greater_than():
    """Test value of last key in row is None when an excess number of fields is supplied."""
    fieldnames = list(ascii_uppercase)[:12]
    reader = Clumper.read_csv("tests/data/monopoly.csv", fieldnames=fieldnames)
    assert reader.select(fieldnames[-1]).head(1).equals([{"L": None}])
