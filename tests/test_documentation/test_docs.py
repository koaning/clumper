import pathlib
import pytest

from mktestdocs import check_md_file

paths = ["docs/index.md", "README.md"]
globbed = [str(_) for _ in pathlib.Path("docs/examples").glob("*.md")]


@pytest.mark.parametrize("fpath", paths + globbed, ids=str)
def test_files_good(fpath):
    """Confirm the python code in markdown files run"""
    check_md_file(fpath=fpath)
