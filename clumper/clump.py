from functools import reduce

from clumper.aggregation import agg


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

    def __init__(self, blob):
        self.blob = blob.copy()

    def __len__(self):
        return len(self.blob)

    def __iter__(self):
        return self.blob.__iter__()

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

    def mutate(self, **kwargs):
        """
        Adds or overrides key-value pairs in the collection of dictionaries.

        Arguments:
            kwargs: keyword arguments of keyname/function-pairs

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

    def sort(self, key, reverse=False):
        """
        Allows you to sort the collection of dictionaries.

        Arguments:
            key: the number of items to grab
            reverse: the number of items to grab

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

    def agg(self, **kwargs):
        """
        Does an aggregation on a collection of dictionaries.

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
        ```
        """
        bad_names = [
            fname for k, (col, fname) in kwargs.items() if fname not in agg.keys()
        ]
        if len(bad_names) > 0:
            raise ValueError(
                f"Allowed aggregation functions are: {agg.keys()}. These don't mix: {bad_names}"
            )
        result = {k: agg[f](col, self.copy()) for k, (col, f) in kwargs.items()}
        return Clumper([result])
