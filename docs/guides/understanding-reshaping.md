Because sequences of nested data really come in all sorts
of shapes and sizes this library offers verbs to help you
reshape the data into different formats. This document will
demonstrate how these verbs work.

## Explode

Sometimes you'll have data that is nested as a list of values.
If you'd like to expand such a list of values you can use
`.explode()`.

![](../img/explode.png)

```python
from clumper import Clumper

data = [{'a': 1, 'items': [1, 2]}]

new_data = Clumper(data).explode("items").collect()
assert new_data == [{'a': 1, 'items': 1}, {'a': 1, 'items': 2}]

new_data = Clumper(data).explode(item="items").collect()
assert new_data == [{'a': 1, 'item': 1}, {'a': 1, 'item': 2}]
```

Note how the syntax allows you to either explode the values
assigning they to the old keyname or to directly rename
this field.
