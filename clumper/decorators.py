from functools import wraps, reduce


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
        results = [method(s, *args, **kwargs) for s in clumper.subsets()]
        blob = reduce(lambda a, b: a + b, [c.collect() for c in results])
        blob_with_keys = [{**s, **b} for s, b in zip(clumper.group_combos(), blob)]
        return clumper.create_new(blob_with_keys)

    return wrapped
