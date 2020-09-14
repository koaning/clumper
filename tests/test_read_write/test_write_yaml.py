from clumper import Clumper


def test_local_read_write_content_same(tmp_path):
    """Test that an error is raised if the written JSON file is not the same as what is read locally"""
    path = str(tmp_path / "pokemon_copy.json")
    writer = Clumper.read_yaml("tests/data/demo-nested.yml")
    writer.write_yaml(path)
    reader = Clumper.read_yaml(path)
    assert reader.collect() == writer.collect()
