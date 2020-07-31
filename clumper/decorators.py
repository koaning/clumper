from functools import wraps, reduce
from copy import deepcopy


def return_value_if_empty(value=None):
    """
    This decorator ensures that if an aggregation column does not
    exist that we return the appropriate value.
    """

    def decorator_return(method):
        @wraps(method)
        def wrapped(clumper, col):
            if len([b for b in clumper if col in b.keys()]) == 0:
                return value
            return method(clumper, col)

        return wrapped

    return decorator_return


def grouped(method):
    """
    Handles the behavior when a group is present on a clumper object.
    """

    @wraps(method)
    def wrapped(clumper, *args, **kwargs):
        if len(clumper.groups) == 0:
            return method(clumper, *args, **kwargs)

        # You may note the deepcopy() here in the keyword arguments. This is done
        # such that state-ful functions (like `row_number`) automatically reset.
        results = [method(s, *args, **deepcopy(kwargs)) for s in clumper._subsets()]
        blob = reduce(lambda a, b: a + b, [c.collect() for c in results])

        # We need to make sure the grouping keys are still available when we do "agg".
        if method.__name__ == "agg":
            blob = [{**s, **b} for s, b in zip(clumper._group_combos(), blob)]
        return clumper._create_new(blob)

    return wrapped


def dict_collection_only(method):
    """
    Handles the behavior when a group is present on a clumper object.
    """

    @wraps(method)
    def wrapped(clumper, *args, **kwargs):
        if not clumper.only_has_dictionaries:
            non_dict = next(d for d in clumper if not isinstance(d, dict))
            raise ValueError(
                f"The `{method}` won't work unless all items are dictionaries. Found: {non_dict}."
            )
        return method(clumper, *args, **kwargs)

    return wrapped
