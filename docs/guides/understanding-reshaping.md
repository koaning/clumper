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

clumper = Clumper(data).explode("items")
assert clumper.equals([{'a': 1, 'items': 1}, {'a': 1, 'items': 2}])

new_data = Clumper(data).explode(item="items").collect()
assert clumper.equals([{'a': 1, 'item': 1}, {'a': 1, 'item': 2}])
```

Note how the syntax allows you to either explode the values,
assigning them to the old keyname or to directly rename
this field. You can also pass multiple keys in a single command.

```python
from clumper import Clumper

data = [{'a': 1, 'items': [1, 2], 'values':[3, 4]}]

clumper = Clumper(data).explode("items", "values")
expected = [
    {'a': 1, 'items': 1, 'values': 3},
    {'a': 1, 'items': 1, 'values': 4},
    {'a': 1, 'items': 2, 'values': 3},
    {'a': 1, 'items': 2, 'values': 4}
]
assert clumper.equals(expected)

new_data = Clumper(data).explode(item="items", val="values").collect()
expected = [
    {'a': 1, 'item': 1, 'val': 3},
    {'a': 1, 'item': 1, 'val': 4},
    {'a': 1, 'item': 2, 'val': 3},
    {'a': 1, 'item': 2, 'val': 4}
]
assert clumper.equals(expected)
```

There are a few extra verbs and use-cases of verbs that
are worth highlighting.

## Single Dictionaries

Sometimes you're dealing with json data that isn't a list of dictionaries. You
should be aware that you may want to read in the data differently. You can keep
the data as a dictionary or automatically wrap it as a list by tweaking the `listify`
parameter. This is available on every `.read_<format>`-method.

### Listify = True

```python
from clumper import Clumper

example1 = Clumper.read_yaml("tests/data/demo-nested.yml")
expected1 = [
    {
        'nested1': [
            {'item': 1, 'value': 'a'},
            {'item': 2, 'value': 'b'},
            {'item': 3, 'value': 'c'}
        ],
        'nested2': [
            {'item': 1, 'value': 'a'},
            {'item': 2, 'value': 'b'},
            {'item': 3, 'value': 'c'}
        ]
    }
]
assert example1.equals(expected1)
```

### Listify = False

```python
from clumper import Clumper
example2 = Clumper.read_yaml("tests/data/demo-nested.yml", listify=False)
expected2 = {
    'nested1': [
        {'item': 1, 'value': 'a'},
        {'item': 2, 'value': 'b'},
        {'item': 3, 'value': 'c'}
    ],
    'nested2': [
        {'item': 1, 'value': 'a'},
        {'item': 2, 'value': 'b'},
        {'item': 3, 'value': 'c'}
    ]
}
assert example2.equals(expected2)
```

## Flatten Keys

In the "list-like dictionary" scenarios you might want to use `.flatten_keys`.
This method flattens the keys in the data.

![](../img/flatten_keys.png)

```python
from clumper import Clumper

data = {
  'feature_1': {'propery_1': 1, 'property_2': 2},
  'feature_2': {'propery_1': 3, 'property_2': 4},
  'feature_3': {'propery_1': 5, 'property_2': 6},
}

expected = [
    {'propery_1': 1, 'property_2': 2, 'key': 'feature_1'},
    {'propery_1': 3, 'property_2': 4, 'key': 'feature_2'},
    {'propery_1': 5, 'property_2': 6, 'key': 'feature_3'}
]

assert Clumper(data, listify=False).flatten_keys().collect() == expected
```

## Unpack

The `unpack` verb is very similar to `explode` but here we expect a list of
dictionaries as opposed to a list of values.

```python
from clumper import Clumper

list_dicts = {
    'a': 1,
    'rows': [{'b': 2, 'c': 3}, {'b': 3}, {'b': 4}]
}

result = Clumper(list_dicts).unpack('rows').collect()

expected = [
    {'a': 1, 'b': 2, 'c': 3},
    {'a': 1, 'b': 3},
    {'a': 1, 'b': 4}
]

assert result == expected
```

## Remove Duplicates

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
