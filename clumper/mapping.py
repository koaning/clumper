"""
This is where we store functions that might help
users with any "map"-kind of step.
"""


def row_number():
    """
    This stateful function can be used to calculate row numbers
    on dictionaries.

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
    i = 0

    def incr(_):
        nonlocal i
        i += 1
        return i

    return incr
