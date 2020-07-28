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
        Selects a subset of the key-value pairs in each dictionary in the collection.

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

    def collect(self):
        """
        Returns a list instead of a `Clumper` object.
        """
        return self.blob
