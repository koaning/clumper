This document is to help give you an overview of what kind of verbs are in this library. They're in essense just methods but they imply a general pattern.

## Advanced: Dict vs. Anything

Although this library has lists of dictionaries in mind,
we actually don't force this on you. We just assume a sequence
as input and from here it's your responsibility to come up
with reasonable lambda functions for the verbs. Most verbs are flexible enough that they don't assume the lambda functions to act on dictionaries.

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

### Character Example

Here we start out with a sequence of letters
and we turn it into a collection of dictionaries.

```python
from clumper import Clumper

(Clumper('abcedfghijklmnopqrstuvwxyz')
  .map(lambda c: {'char': c, 'ord': ord(c)}))
```

### Verbs that need Dictionaries

There's a short list verbs that have some restrictions

- **.select()** needs to select keys so the sequences must contain dictionaries
- **.drop()** needs to remove keys so the sequences must contain dictionaries
- **.agg()** needs a collection of dictionaries to construct aggregations. If you
really need this feature for non-dictionary sequences consider **.reduce()**.
- **.mutate()** is really flexible in terms of input that it
accepts but it will always produce a dictionary as output. If you really need a non-dictionary output, consider **.map()**
