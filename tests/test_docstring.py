import pytest
from clumper import Clumper


def handle_docstring(doc):
    start = doc.find("```python\n")
    end = doc.find("```\n")
    if start != -1:
        if end != -1:
            code_part = doc[(start + 10) : end].replace("        ", "")
            print(code_part)
            exec(code_part)


@pytest.mark.parametrize("m", [m for m in dir(Clumper) if "__" not in m])
def test_docs(m):
    handle_docstring(getattr(Clumper, m).__doc__)
