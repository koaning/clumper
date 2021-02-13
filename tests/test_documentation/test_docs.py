import pathlib
import pytest

from mktestdocs import check_md_file

paths = ["docs/index.md", "README.md"] + list(
    pathlib.Path("docs/examples").glob("*.md")
)


@pytest.mark.parametrize("fpath", paths, ids=str)
def test_files_good(fpath):
    check_md_file(fpath=fpath)
