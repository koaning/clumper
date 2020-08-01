---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

Please add a reproducible codeblock if possible.

We've included some methods to our library to make this
relatively easy. Here's an example of a reproducible code-block.

```python
from clumper import Clumper

data = [{"a": 1}, {"a": 2}]

clump = Clumper(data)
expected = [{"a": 1}, {"a": 2}]
assert clump.equals(expected)
```

**Additional context**

Feel free to mention your operating system and python version.
