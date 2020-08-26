import pytest
from clumper import Clumper


def temp_file(tmp_path):
    """helper function to create temporary file."""
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "nulls.csv"
    return path


def test_write_csv(tmp_path):
    path = temp_file(tmp_path)
    Clumper.read_csv("tests/data/monopoly.csv").write_csv(path)
    reader = Clumper.read_csv(path)
    assert Clumper.read_csv("tests/data/monopoly.csv").collect() == reader.collect()


def test_write_csv_append_mode(tmp_path):
    """Test that the append mode works."""
    path = temp_file(tmp_path)
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
    path = temp_file(tmp_path)
    Clumper(data).write_csv(path)
    reader = Clumper.read_csv(path, na_values="ignore")
    assert Clumper(data).collect() == reader.collect()


def test_write_csv_fieldnames(data, tmp_path):
    """Test that fieldnames of Clumper match the headers in the exported csv file"""
    path = temp_file(tmp_path)
    Clumper(data).write_csv(path)
    reader = Clumper.read_csv(path)
    assert not set(Clumper(data).keys()).difference(reader.keys())


def test_write_csv_n_positive(data, tmp_path):
    """Test that the correct number of rows is exported"""
    path = temp_file(tmp_path)
    Clumper(data).head(n=10).write_csv(path)
    reader = Clumper.read_csv(path, na_values="ignore")
    assert Clumper(data).head(n=10).collect() == reader.collect()


def test_write_missing_keys(tmp_path):
    """Test that function works with missing keys."""
    data2 = [{"a": "1", "b": "2"}, {"c": "3"}]
    path = temp_file(tmp_path)
    Clumper(data2).write_csv(path)
    reader = Clumper.read_csv(path)
    assert Clumper(data2).equals(reader)


data_type = [
    [{"a": 1, "b": 2}, {"a": 2, "b": 3, "c": 4}, {"a": 1, "b": 6}],
    [{"a": 1, "b": 2}, {"c": 3}],
    [{"a": 1, "b": 2}, {"a": 3, "b": 3}, {"a": 2, "b": 1}],
    [
        {"Name": "Sam", "Age": 34, "City": "Sydney"},
        {"Name": "Ade", "Age": 31, "City": "Lagos"},
        {"Name": "Uche", "Age": 16, "City": "Abuja"},
        {"Name": "Maleek", "Age": 32, "City": "Kano"},
        {"Name": "Ragnar", "Age": 33, "City": "Reykjavik"},
        {"Name": "Zeus", "Age": 35, "City": "Athens"},
    ],
    [
        {"V4": "A", "V1": 0, "V2": 3},
        {"V4": "A", "V1": 0, "V2": 4},
        {"V4": "A", "V1": 0, "V2": 7},
        {"V4": "B", "V1": 4, "V2": 0},
        {"V4": "B", "V1": 4, "V2": 8},
        {"V4": "B", "V1": 1, "V2": 5},
        {"V4": "C", "V1": 4, "V2": 5},
        {"V4": "C", "V1": 1, "V2": 0},
        {"V4": "C", "V1": 1, "V2": 9},
    ],
]

data_type = tuple(
    zip(data_type, ["int", "int", "int", {"Age": "int"}, {"V1": "int", "V2": "int"}])
)


@pytest.mark.parametrize("dtype_data,dtype", data_type)
def test_read_csv(dtype_data, dtype, tmp_path):
    """Test that the correct dtype is returned when dtype argument is not None."""
    path = temp_file(tmp_path)
    Clumper(dtype_data).write_csv(path)
    reader = Clumper.read_csv(path, dtype=dtype)
    assert Clumper(dtype_data).equals(reader)
