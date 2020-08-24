import pytest
from clumper import Clumper


def test_write_csv(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "monopoly_copy.csv"
    Clumper.read_csv("tests/data/monopoly.csv").write_csv(path)
    reader = Clumper.read_csv(path)
    assert Clumper.read_csv("tests/data/monopoly.csv").collect() == reader.collect()


def test_write_csv_append_mode(tmp_path):
    """Test that the append mode works."""
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "monopoly_copy.csv"
    Clumper.read_csv("tests/data/monopoly.csv").write_csv(path)
    Clumper.read_csv("tests/data/monopoly.csv").write_csv(path, mode="a")
    reader = Clumper.read_csv(path)
    # the header is appended as well, hence the +1
    assert len(reader) == (2 * len(Clumper.read_csv("tests/data/monopoly.csv"))) + 1


@pytest.fixture()
def data():
    return [
        {"One": "a", "Two": "1", "Three": "one"},
        {"One": "b", "Two": "2", "Three": "two"},
        {"One": "", "Two": "3", "Three": "three"},
        {"One": "d", "Two": "4", "Three": ""},
        {"One": "e", "Two": "5", "Three": "five"},
        {"One": "", "Two": "6", "Three": ""},
        {"One": "g", "Two": "7", "Three": "seven"},
    ]


def test_write_empty_csv(data, tmp_path):
    """Test that null cells are exported correctly as empty strings"""
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    Clumper(data).write_csv(path)
    reader = Clumper.read_csv(path, na_values="ignore")
    assert Clumper(data).collect() == reader.collect()


def test_write_csv_fieldnames(data, tmp_path):
    """Test that fieldnames of Clumper match the headers in the exported csv file"""
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    Clumper(data).write_csv(path)
    reader = Clumper.read_csv(path)
    assert not set(Clumper(data).keys()).difference(reader.keys())


def test_write_csv_n_positive(data, tmp_path):
    """Test that the correct number of rows is exported"""
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    Clumper(data).head(n=10).write_csv(path)
    reader = Clumper.read_csv(path, na_values="ignore")
    assert Clumper(data).head(n=10).collect() == reader.collect()


def test_write_missing_keys(tmp_path):
    """Test that function works with missing keys."""
    data2 = [{"a": "1", "b": "2"}, {"c": "3"}]
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    Clumper(data2).write_csv(path)
    reader = Clumper.read_csv(path)
    assert Clumper(data2).equals(reader)


def test_write_dtype(tmp_path):
    """Test that the correct dtype is returned when dtype argument is not None."""
    data2 = [{"a": 1, "b": 2}, {"c": 3}]
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    Clumper(data2).write_csv(path)
    reader = Clumper.read_csv(path, dtype="int")
    assert Clumper(data2).equals(reader)
