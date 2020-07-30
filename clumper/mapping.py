"""
This is where we store functions that might help
users with any "map"-kind of step.
"""


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
