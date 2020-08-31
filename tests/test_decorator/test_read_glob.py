from clumper import Clumper


def test_read_multiple_jsonl(tmp_path):
    """
    Test that multiple files can be read with glob
    """

    writer = Clumper.read_jsonl("tests/data/cards.jsonl")
    writer.write_jsonl(tmp_path / "cards_copy.jsonl")
    writer.write_jsonl(tmp_path / "cards_copy_2.jsonl")

    reader = Clumper.read_jsonl(tmp_path.glob("*.jsonl"))
    assert len(reader) == 2 * len(writer)
