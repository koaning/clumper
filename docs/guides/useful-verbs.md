There are a few extra verbs and use-cases of verbs that
are worth highlighting.

## Duplicates

Removing duplicates is tricky via `.keep()` so instead we've
created a method for this usecase.

![](../img/drop_duplicates.png)

```python
from clumper import Clumper

data = [{"a": 1}, {"a": 2}, {"a": 2}]
clump = Clumper(data).drop_duplicates()
expected = [{"a": 1}, {"a": 2}]

assert clump.equals(expected)
```
