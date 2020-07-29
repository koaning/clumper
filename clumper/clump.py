from functools import reduce
import itertools as it

from clumper.decorators import return_value_if_empty, grouped


class Clumper:
    """
    This object adds methods to a list of dictionaries that make
    it nicer to explore.

    Usage:

    ```python
    from clumper import Clumper

    list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

    c = Clumper(list_dicts)
    ```
    """

    def __init__(self, blob, groups=tuple()):
        self.blob = blob.copy()
        self.groups = groups

    def __len__(self):
        return len(self.blob)

    def __iter__(self):
        return self.blob.__iter__()

    def create_new(self, blob):
        """
        Creates a new collection of data while preserving settings of the
        current collection (most notably, `groups`).
        """
        return Clumper(blob, groups=self.groups)

    def group_by(self, *cols):
        """
        Sets a group on this clumper object or overrides a previous setting.
        """
        self.groups = cols
        return self

    def ungroup(self):
        """
        Removes all grouping.
        """
        self.groups = tuple()
        return self

    @grouped
    def agg(self, **kwargs):
        """
        Does an aggregation on a collection of dictionaries.

        Warning:
            This method is aware of groups. Expect different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3},
            {'a': 3}
        ]

        (Clumper(list_dicts)
          .agg(mean_a=('a', 'mean'),
               min_b=('b', 'min'),
               max_b=('b', 'max'))
          .collect())

        another_list_dicts = [
            {'a': 1, 'c': 'a'},
            {'a': 2, 'c': 'b'},
            {'a': 3, 'c': 'a'}
        ]

        (Clumper(another_list_dicts)
          .group_by('c')
          .agg(mean_a=('a', 'mean'),
               uniq_a=('a', 'unique'))
          .collect())
        ```
        """
        funcs = {
            "mean": self.mean,
            "count": self.count,
            "unique": self.unique,
            "n_unique": self.n_unique,
            "sum": self.sum,
            "min": self.min,
            "max": self.max,
        }
        res = {name: funcs[func_str](col) for name, (col, func_str) in kwargs.items()}
        return Clumper([res])

    def subsets(self):
        result = []
        for gc in self.group_combos():
            subset = self.copy()
            for key, value in gc.items():
                subset = subset.keep(lambda d: d[key] == value)
            result.append(subset)
        return result

    def concat(self, *other):
        """
        Concatenate two or more `Clumper` objects together.
        """
        return Clumper(self.blob + other.blob)

    def group_combos(self):
        """
        Returns a dictionary of group-value/clumper pairs.
        """
        combinations = [
            comb for comb in it.product(*[self.unique(c) for c in self.groups])
        ]
        return [{k: v for k, v in zip(self.groups, comb)} for comb in combinations]

    def keep(self, *funcs):
        """
        Allows you to select which items to keep and which items to remove.

        Arguments:
            funcs: functions that indicate which items to keep

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        (Clumper(list_dicts)
          .keep(lambda d: d['a'] >= 3)
          .collect())
        ```
        """
        data = self.blob.copy()
        for func in funcs:
            data = [d for d in data if func(d)]
        return Clumper(data)

    def head(self, n=5):
        """
        Selects the top `n` items from the collection.

        Arguments:
            n: the number of items to grab

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        (Clumper(list_dicts)
          .head(2)
          .collect())
        ```
        """
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be a positive integer, got {n}")
        n = min(n, len(self))
        return Clumper([self.blob[i] for i in range(n)])

    def tail(self, n=5):
        """
        Selects the top `n` items from the collection.

        Arguments:
            n: the number of items to grab

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        (Clumper(list_dicts)
          .tail(2)
          .collect())
        ```
        """
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be positive, got {n}")
        n = min(n, len(self))
        return Clumper([self.blob[-i] for i in range(len(self) - n, len(self))])

    def select(self, *keys):
        """
        Selects a subset of the keys in each item in the collection.

        Arguments:
            keys: the keys to keep

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        (Clumper(list_dicts)
          .select('a', 'b')
          .collect())
        ```
        """
        return Clumper([{k: d[k] for k in keys} for d in self.blob])

    def drop(self, *keys):
        """
        Removes a subset of keys from each item in the collection.

        Arguments:
            keys: the keys to remove

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        (Clumper(list_dicts)
          .drop('a', 'c')
          .collect())
        ```
        """
        return Clumper(
            [{k: v for k, v in d.items() if k not in keys} for d in self.blob]
        )

    @grouped
    def mutate(self, **kwargs):
        """
        Adds or overrides key-value pairs in the collection of dictionaries.

        Arguments:
            kwargs: keyword arguments of keyname/function-pairs

        Warning:
            This method is aware of groups. There may be different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        (Clumper(list_dicts)
          .mutate(c=lambda d: d['a'] + d['b'],
                  s=lambda d: d['a'] + d['b'] + d['c'])
          .collect())
        ```
        """
        data = []
        for d in self.blob.copy():
            new = {k: v for k, v in d.items()}
            for key, func in kwargs.items():
                new[key] = func(new)
            data.append(new)
        return Clumper(data)

    @grouped
    def sort(self, key, reverse=False):
        """
        Allows you to sort the collection of dictionaries.

        Arguments:
            key: the number of items to grab
            reverse: the number of items to grab

        Warning:
            This method is aware of groups. Expect different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 3},
            {'a': 2, 'b': 1}]

        (Clumper(list_dicts)
          .sort(lambda d: d['a'])
          .collect())

        (Clumper(list_dicts)
          .sort(lambda d: d['b'], reverse=True)
          .collect())
        ```
        """
        return Clumper(sorted(self.blob, key=key, reverse=reverse))

    def map(self, func):
        """
        Directly map one item to another one using a function.
        If you're dealing with dictionaries, consider using
        `mutate` instead.

        Arguments:
            func: the function that will map each item

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}]

        (Clumper(list_dicts)
          .map(lambda d: {'a': d['a'], 'b': 1})
          .collect())
        ```
        """
        return Clumper([func(d) for d in self.blob])

    def reduce(self, **kwargs):
        """
        Reduce the collection using reducing functions.

        Arguments:
            kwargs: key-function pairs

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [1, 2, 3, 4, 5]

        (Clumper(list_dicts)
          .reduce(sum_a = lambda x,y: x + y,
                  min_a = lambda x,y: min(x, y),
                  max_a = lambda x,y: max(x, y))
          .collect())
        ```
        """
        return Clumper(
            [{k: reduce(func, [b for b in self.blob]) for k, func in kwargs.items()}]
        )

    def pipe(self, func, *args, **kwargs):
        """
        Applies a function to the `Clumper` object in a chain-able manner.

        Arguments:
            func: function to apply
            args: arguments that will be passed to the function
            kwargs: keyword-arguments that will be passed to the function

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': i} for i in range(100)]

        def remove_outliers(clump, min_a=20, max_a=80):
            return (clump
                      .keep(lambda d: d['a'] >= min_a,
                            lambda d: d['a'] <= max_a))

        (Clumper(list_dicts)
          .pipe(remove_outliers, min_a=10, max_a=90)
          .collect())
        ```
        """
        return func(self, *args, **kwargs)

    def collect(self):
        """
        Returns a list instead of a `Clumper` object.
        """
        return self.blob

    def copy(self):
        """
        Makes a copy of the collection.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': i} for i in range(100)]

        c1 = Clumper(list_dicts)
        c2 = c1.copy()
        assert id(c1) != id(c2)
        ```
        """
        return Clumper([d for d in self.blob])

    @return_value_if_empty(value=None)
    def sum(self, col):
        """
        Give the sum of the values that belong to a key.
        """
        return sum([d[col] for d in self if col in d.keys()])

    @return_value_if_empty(value=None)
    def mean(self, col):
        """
        Give the mean of the values that belong to a key.
        """
        s = sum([d[col] for d in self if col in d.keys()])
        return s / len(self)

    @return_value_if_empty(value=None)
    def count(self, col):
        """
        Counts how often a key appears in the collection.
        """
        return len([1 for d in self if col in d.keys()])

    @return_value_if_empty(value=0)
    def n_unique(self, col):
        """
        Returns number of unique values that a key has.
        """
        return len({d[col] for d in self if col in d.keys()})

    @return_value_if_empty(value=None)
    def min(self, col):
        """
        Returns minimum value that a key has.
        """
        return min([d[col] for d in self if col in d.keys()])

    @return_value_if_empty(value=None)
    def max(self, col):
        """
        Returns maximum value that a key has.
        """
        return max({d[col] for d in self if col in d.keys()})

    @return_value_if_empty(value=[])
    def unique(self, col):
        """
        Returns a set of unique values that a key has.
        """
        return list({d[col] for d in self if col in d.keys()})
