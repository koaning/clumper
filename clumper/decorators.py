from functools import wraps, reduce
from copy import deepcopy
import pathlib
import inspect


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


def multifile(param_name="path"):
    def decorator(f):
        sig = inspect.signature(f)

        if param_name not in sig.parameters:
            raise ValueError(f"Wrapped function has no parameter '{param_name}'")

        @wraps(f)
        def wrapper(*args, **kwargs):
            bound_arguments = sig.bind(*args, **kwargs)

            bound_arguments.apply_defaults()

            path = bound_arguments.arguments[param_name]

            # Using this path.Glob, extract all the files if any
            collected_clumpers = []

            if isinstance(path, str):
                if path.startswith("https:") or path.startswith("http:"):
                    return f(*args, **kwargs)
                else:
                    path = pathlib.Path().glob(path)

            for p in path:
                # Set the path variable to p
                bound_arguments.arguments[param_name] = str(p)
                # Call the reader function and create the Clumper object
                collected_clumpers.append(
                    f(*bound_arguments.args, *bound_arguments.kwargs)
                )

            # Combine them by concating their dict
            blob = reduce(
                lambda a, b: a + b,
                [c.collect() for c in collected_clumpers if len(c) > 0],
            )

            # Create a new object Clumper object based on the first element
            clumper_object = collected_clumpers[0]._create_new(blob)

            return clumper_object

        return wrapper

    return decorator


def print_callback(val):
    print(f"Value is {val}")


def read_glob(method, path, *args, **kwargs):

    collected_clumpers = []

    # If arg is string then convert it to Path.glob
    if isinstance(path, str):
        path = pathlib.Path().glob(path)

    # Assuming that all file path fits in the memory
    path_list = list(path)
    assert len(path_list) > 0, f"There are no file(s) given pattern"
    for p in path_list:
        collected_clumpers.append(method(str(p), *args, **kwargs))
    blob = reduce(lambda a, b: a + b, [c.collect() for c in collected_clumpers])
    clumper_object = collected_clumpers[0]._create_new(blob)
    return clumper_object
