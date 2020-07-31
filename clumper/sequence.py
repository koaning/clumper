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

    ![](../img/row_number.png)

    Usage:

    ```python
    from clumper import Clumper
    from clumper.sequence import row_number

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
    This stateful function can be used to create a moving window
    over a key.

    ![](../img/rolling.png)

    Arguments:
        key: the key to apply the smoothing to
        window: the size of the window to create

    Usage:

    ```python
    from clumper import Clumper
    from clumper.sequence import rolling

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
    This stateful function can be used to expand a key into a large list containing all the seen values.

    ![](../img/expanding.png)

    Arguments:
        key: the key to apply the smoothing to

    Usage:

    ```python
    from clumper import Clumper
    from clumper.sequence import expanding

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
    This stateful function can be used to calculate row numbers. Uses exponential smoothing.

    ![](../img/smoothing.png)

    Arguments:
        key: the key to apply the smoothing to
        weight: exponential smoothing parameter, if 1.0 then we don't listen to the past anymore

    Usage:

    ```python
    from clumper import Clumper
    from clumper.sequence import smoothing

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4}
    ]

    (Clumper(list_dicts)
      .mutate(s1=smoothing(key='a', weight=0.5),
              s2=smoothing(key='a', weight=0.9))
      .collect())
    ```
    """

    def __init__(self, key=None, weight=0.5):
        self.key = key
        self.state = None
        if (weight < 0) | (weight > 1):
            raise ValueError(
                f"The `weight` param for `smoothing` needs to be in [0, 1]. Got: {weight}."
            )
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


class impute:
    """
    This stateful function can be used to calculate row numbers. Uses exponential smoothing.

    Arguments:
        key: the key to apply the smoothing to
        strategy: the strategy to apply
        fallback: if the strategy fails, what value to use

    Usage:

    ```python
    from clumper import Clumper
    from clumper.sequence import impute

    list_dicts = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3},
        {'a': 4, 'b': 6},
        {'a': 5},
    ]

    (Clumper(list_dicts)
      .mutate(b=impute('b', strategy='prev'),
              c=lambda d: d['a'] + d['b'])
      .collect())

    (Clumper(list_dicts)
      .mutate(b=impute('b', strategy='value', fallback=0))
      .collect())
    ```
    """

    def __init__(self, key, strategy="prev", fallback=None):
        self.key = key
        self.strategy = strategy
        allowed_strategies = ["prev", "value"]
        if strategy not in allowed_strategies:
            raise ValueError(
                f"`impute` only allows {allowed_strategies} as strategies, got: '{strategy}'.'"
            )
        self.fallback = fallback
        self.state = None

    def grab_key(self, new):
        if isinstance(self.key, str):
            return new[self.key]
        if isinstance(self.key, Callable):
            return self.key(new)
        raise ValueError(
            f"The `imputer` saw {new} and could not apply key: {self.key}."
        )

    def is_missing(self, new):
        try:
            _ = self.grab_key(new)
            return False
        except KeyError:
            return True

    def handle_missing(self):
        if self.strategy == "prev":
            return self.fallback if not self.state else self.state
        if self.strategy == "value":
            return self.fallback

    def update(self, new):
        if self.strategy == "prev":
            self.state = self.grab_key(new)

    def __call__(self, new):
        if self.is_missing(new):
            return self.handle_missing()
        self.update(new)
        return self.grab_key(new)


__all__ = ("row_number", "rolling", "expanding", "impute")
