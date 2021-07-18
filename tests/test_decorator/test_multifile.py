from clumper import Clumper
import pytest
from pathlib import Path


def test_non_existent_pattern(tmp_path):
    """When there's no paths that exist, throw an error"""
    with pytest.raises(ValueError):
        Clumper.read_json(str(tmp_path / "*.json"))
        Clumper.read_json(list(Path(tmp_path).glob("*.json")))


@pytest.mark.parametrize("copies", [1, 5, 10])
def test_read_multiple_jsonl(tmp_path, copies):
    """
    Test that jsonl files can be read given a pattern
    """

    writer = Clumper.read_jsonl("tests/data/cards.jsonl")

    for i in range(copies):
        writer.write_jsonl(tmp_path / f"cards_copy_{i}.jsonl")

    reader = Clumper.read_jsonl(str(tmp_path / "*.jsonl"))
    assert len(reader) == copies * len(writer)

    reader = Clumper.read_jsonl(list(Path(tmp_path).glob("*.jsonl")))
    assert len(reader) == copies * len(writer)


@pytest.mark.parametrize("copies", [1, 5, 10])
def test_read_multiple_json(tmp_path, copies):
    """
    Test that json files can be read given a pattern
    """

    writer = Clumper.read_json("tests/data/pokemon.json")

    for i in range(copies):
        writer.write_json(tmp_path / f"pokemon_copy_{i}.json")

    reader = Clumper.read_json(str(tmp_path / "*.json"))
    assert len(reader) == copies * len(writer)

    reader = Clumper.read_json(list(Path(tmp_path).glob("*.json")))
    assert len(reader) == copies * len(writer)


@pytest.mark.parametrize("copies", [1, 5, 10])
def test_read_multiple_csv(tmp_path, copies):
    """
    Test that csv files can be read given a pattern
    """

    writer = Clumper.read_csv("tests/data/monopoly.csv")

    for i in range(copies):
        writer.write_csv(tmp_path / f"monopoly_copy_{i}.csv")

    reader = Clumper.read_csv(str(tmp_path / "*.csv"))
    assert len(reader) == copies * len(writer)

    reader = Clumper.read_csv(list(Path(tmp_path).glob("*.csv")))
    assert len(reader) == copies * len(writer)


@pytest.mark.parametrize("copies", [1, 5, 10])
def test_read_multiple_yaml(tmp_path, copies):
    """
    Test that yaml files can be read given a pattern
    """

    writer = Clumper.read_yaml("tests/data/demo-nested.yml")

    for i in range(copies):
        writer.write_yaml(tmp_path / f"demo-nested-{i}.yml")

    reader = Clumper.read_yaml(str(tmp_path / "*.yml"))
    assert len(reader) == copies * len(writer)

    reader = Clumper.read_yaml(list(Path(tmp_path).glob("*.yml")))
    assert len(reader) == copies * len(writer)
