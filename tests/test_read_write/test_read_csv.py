import pytest
from clumper import Clumper


@pytest.mark.parametrize(
    "path, delimiter, nrows, fieldnames, length",
    [
        ("tests/monopoly.csv", ",", None, None, 22),
        ("tests/monopoly.csv", ",", 10, None, 10),
        (
            "tests/monopoly.csv",
            ",",
            10,
            [
                "name",
                "ogun_rent",
                "ragnar_house_1",
                "house_2",
                "zeus_house_3",
                "house_4",
                "hotel",
                "deed_cost",
                "house_cost",
                "euripides_color",
                "tile",
            ],
            10,
        ),
        ("https://calmcode.io/datasets/monopoly.csv", ",", None, None, 22),
        ("https://calmcode.io/datasets/monopoly.csv", ",", 15, None, 15),
        (
            "https://calmcode.io/datasets/monopoly.csv",
            ",",
            15,
            [
                "namaste",
                "rernt",
                "house1",
                "house2",
                "house3",
                "house4",
                "hotell",
                "deed_cost",
                "house_cost",
                "color",
                "tille",
            ],
            15,
        ),
    ],
)
def test_read_csv(path, delimiter, nrows, fieldnames, length):
    "Test that the length of clumper matches the total number of rows in the csv. Also test that the correct field names and number are returned"
    clump = Clumper.read_csv(
        path=path, delimiter=delimiter, nrows=nrows, fieldnames=fieldnames
    )
    field_names = {
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
    }
    assert len(clump) == length
    if not fieldnames:
        assert not field_names.difference(clump.keys())
    else:
        assert not set(fieldnames).difference(clump.keys())


def test_wrong_delimiter():
    "Test that an error is raised if a wrong delimiter is supplied."
    with pytest.raises(TypeError):
        Clumper.read_csv("tests/monopoly.csv", delimiter=", ")


def test_read_csv_negative_nrows():
    "Test that an error is raised if nrows is negative."
    with pytest.raises(ValueError):
        Clumper.read_csv("tests/monopoly.csv", nrows=-5)
