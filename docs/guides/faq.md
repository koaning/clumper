### Usecase

#### When should I use `Clumper`?

This package might solve some problems for you if:

- You're dealing with nested data.
- You're dealing with data that's not super big.
- You enjoy using a functional-style of exploring data.

#### When should I not use `Clumper`?

This package might not be the best choice if:

- You're dealing with very large datasets.
- You're dealing with data that strictly

### Library Assumptions

#### How does `Clumper` deal with missing data?

If your datastructure represents a table with rows and columns then you'd
usually denote missing data via something like `NA` or `NaN`. This is common
in SQL but also in numeric libraries like `numpy`. Since this library tries
to focus on json-like data-structures we also deal with it differently.

If you'd be dealing with a csv, you'd consider this example to contain missing data.

```python
list_of_data = [
    {"r": 1, "a": 1.5},
    {"r": 2, "a": None},
    {"r": 3, "a": 2.5}
]
```

Instead, this is how `Clumper` would represent it.

```python
list_of_data = [
    {"r": 1, "a": 1.5},
    {"r": 2},
    {"r": 3, "a": 2.5}
]
```

In this case we have an item where the key `"a"` is acutally missing. In the
previous example we definately had a key but the value was equal to `None`.

## Am I limited to dictionaries?

Although this library has lists of dictionaries in mind,
we actually don't force this on you. We just assume a sequence
as input. From here it's your responsibility to come up
with reasonable lambda functions for the verbs that follow.

Most verbs are flexible enough that they don't assume the
lambda functions to act on dictionaries.

For example. If you look at this code:

```
.sort(lambda d: d)
```

Then you can infer that we're sorting based on whatever
the value in our collection is. It would work on a list
of integers, floats or characters. If you'd instead have:

```
.sort(lambda d: d[0])
```

Then it wouldn't work anymore if `d` is a integer, float
or string but it would work if `d` is a list, tuple or a
dictionary with a key of `0` available.


### Integer Example

Here we take the top 50 numbers from a list and then sort.

```python
from clumper import Clumper

(Clumper(range(100))
  .head(50)
  .sort(lambda d: d, reverse=True))
```

Neither `.head()` nor `.sort()` makes an assumption of the
conents of the `Clumper` collection. Pay attention though that
the `lambda` function inside of `.sort()` is appropriate for the
data in the collection.

### Character Example

Here we start out with a sequence of letters
and we turn it into a collection of dictionaries.

```python
from clumper import Clumper

(Clumper('abcedfghijklmnopqrstuvwxyz')
  .map(lambda c: {'char': c, 'ord': ord(c)}))
```

### Verbs that need Dictionaries

There's a short list of verbs that carry some restrictions

- The **.select()** verb needs to select keys so the sequences must contain dictionaries
- The **.drop()** verb needs to remove keys so the sequences must contain dictionaries
- The **.agg()/.transform()** verbs need a collection of dictionaries to construct aggregations. If you
really need this feature for non-dictionary sequences consider the **.reduce()** method.
- The **.mutate()** verb is really flexible in terms of input that it
accepts but it will always produce a dictionary as output.
If you really need a non-dictionary output, consider the **map()** method.
