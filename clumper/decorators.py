from functools import wraps


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
