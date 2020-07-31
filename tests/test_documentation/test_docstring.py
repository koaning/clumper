import pytest
from clumper import Clumper
from clumper.mappers import row_number, smoothing, expanding, rolling, impute


def handle_docstring(doc, indent):
    """
    This function will read through the docstring and grab
    the first python code block. It will try to execute it.
    If it fails, the calling test should raise a flag.
    """
    if not doc:
        return
    start = doc.find("```python\n")
    end = doc.find("```\n")
    if start != -1:
        if end != -1:
            code_part = doc[(start + 10) : end].replace(" " * indent, "")
            print(code_part)
            exec(code_part)


@pytest.mark.parametrize("m", [m for m in dir(Clumper) if "_" not in m])
def test_clumper_docstrings(m):
    """
    Take the docstring of every method on the `Clumper` class.
    The test passes if the usage examples causes no errors.
    """
    handle_docstring(getattr(Clumper, m).__doc__, indent=8)


@pytest.mark.parametrize("m", [row_number, smoothing, expanding, rolling, impute])
def test_mappers_docstrings(m):
    """
    Take the docstring of every method on the `Clumper` class.
    The test passes if the usage examples causes no errors.
    """
    handle_docstring(m.__doc__, indent=4)
