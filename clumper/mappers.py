"""
A collection of functions to be used in `mutate`/`map`-verbs.
"""

from typing import Callable


def _old_row_number():
    i = 0

    def incr(_):
        nonlocal i
        i += 1
        return i

    return incr


class row_number:
    """
    This stateful function can be used to calculate row numbers.

    Usage:

    ```python
    from clumper import Clumper
    from clumper.mappers import row_number

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4}
    ]

    (Clumper(list_dicts)
      .mutate(r=row_number())
      .collect())
    ```
    """

    def __init__(self):
        self.state = 0

    def __call__(self, _):
        self.state += 1
        return self.state


class rolling:
    """
    This stateful function can be used to calculate row numbers.

    Usage:

    ```python
    from clumper import Clumper
    from clumper.mappers import rolling

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4}
    ]

    (Clumper(list_dicts)
      .mutate(r=rolling(window=2, key='a'))
      .collect())
    ```
    """

    def __init__(self, window=5, key=None):
        self.state = []
        self.window = window
        self.key = key

    def apply_key(self, new):
        if isinstance(self.key, str):
            return new[self.key]
        if isinstance(self.key, Callable):
            return self.key(new)

    def __call__(self, new):
        # we can't append because of mutable state
        self.state = self.state + [self.apply_key(new)]
        if len(self.state) > self.window:
            self.state = self.state[1:]
        return self.state


class expanding:
    """
    This stateful function can be used to calculate row numbers.

    Usage:

    ```python
    from clumper import Clumper
    from clumper.mappers import expanding

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4}
    ]

    (Clumper(list_dicts)
      .mutate(r=expanding(key='a'))
      .collect())
    ```
    """

    def __init__(self, key=None):
        self.state = []
        self.key = key

    def apply_key(self, new):
        if isinstance(self.key, str):
            return new[self.key]
        if isinstance(self.key, Callable):
            return self.key(new)

    def __call__(self, new):
        self.state = self.state + [self.apply_key(new)]
        return self.state


class smoothing:
    """
    This stateful function can be used to calculate row numbers.

    Usage:

    ```python
    from clumper import Clumper
    from clumper.mappers import expanding

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4}
    ]

    (Clumper(list_dicts)
      .mutate(s=smoothing(key='a', weight=0.5))
      .collect())

    (Clumper(list_dicts)
      .mutate(s=smoothing(key='a', weight=0.9))
      .collect())
    ```
    """

    def __init__(self, key=None, weight=0.5):
        self.key = key
        self.state = None
        self.weight = weight

    def apply_key(self, new):
        if isinstance(self.key, str):
            return new[self.key]
        if isinstance(self.key, Callable):
            return self.key(new)

    def __call__(self, new):
        new = self.apply_key(new)
        if not self.state:
            self.state = new
        self.state = self.state * (1 - self.weight) + new * self.weight
        return self.state
