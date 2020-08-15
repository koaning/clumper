import pytest
from clumper import Clumper


def test_read_csv():
    "Test that the length of clumper matches the total number of rows in the csv."
    clump = Clumper.read_csv("tests/iris.csv")
    assert len(clump) == 150


def test_read_csv_url():
    "Test that data is read correctly from url, with the right number of rows."
    clump = Clumper.read_csv("https://calmcode.io/datasets/monopoly.csv")
    assert len(clump) == 22


def test_read_csv_nrows():
    "Test that the length of clumper matches the number of rows requested from the csv."
    clump = Clumper.read_csv("tests/iris.csv", nrows=50)
    assert len(clump) == 50


def test_read_csv_nrows_url():
    "Test that the length of clumper matches the number of rows requested from the url."
    clump = Clumper.read_csv("https://calmcode.io/datasets/monopoly.csv", nrows=10)
    assert len(clump) == 10


def test_wrong_delimiter():
    "Test that an error is raised if a wrong delimiter is supplied."
    with pytest.raises(TypeError):
        Clumper.read_csv("tests/iris.csv", delimiter=", ")


def test_read_csv_negative_nrows():
    "Test that an error is raised if nrows is negative."
    with pytest.raises(ValueError):
        Clumper.read_csv("tests/iris.csv", nrows=-5)
