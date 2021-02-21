from functools import wraps, reduce
from copy import deepcopy
import inspect
from glob import glob
from pathlib import Path


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
    Throws an error if the first element in the Clumper is not a dictionary.
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
    """
    Creates a wrapper around read function to read multiple file given a pattern with at least one * in the path.
    """

    def decorator(f):
        sig = inspect.signature(f)

        if param_name not in sig.parameters:
            raise ValueError(
                f"Reader function {f.__name__} has no parameter '{param_name}'"
            )

        @wraps(f)
        def wrapper(*args, **kwargs):
            bound_arguments = sig.bind(*args, **kwargs)

            bound_arguments.apply_defaults()

            path = bound_arguments.arguments[param_name]

            # If * not in path then let the default function handle it.
            # We are only interested if the path has * in it
            if isinstance(path, str):
                if "*" not in path:
                    return f(*args, **kwargs)
                else:
                    # Else, create a glob out of it
                    path_list = glob(path)

            # Let default function handle single Path objects
            elif isinstance(path, Path):
                return f(*args, **kwargs)

            # Handle a list of Path objects
            elif isinstance(path, (list)):
                path_list = []
                for p in path:
                    if isinstance(p, Path):
                        path_list.append(p)
                    else:
                        raise ValueError(f"Invalid path: {p}")
            else:
                raise ValueError(
                    f"{path} is not a valid string, Path, or list of Paths"
                )

            # No files found given the pattern so raise error
            if len(path_list) == 0:
                raise ValueError(f"No files found given pattern : {path}")

            # Store the parsed clumpers here
            collected_clumpers = []

            # Iterate each path in the glob
            for p in path_list:
                # Set the path variable
                bound_arguments.arguments[param_name] = str(p)
                # Call the underlying reader function
                clumper = f(*bound_arguments.args, **deepcopy(bound_arguments.kwargs))
                # Collect the clumper
                collected_clumpers.append(clumper)

            # Only one object found
            if len(collected_clumpers) == 1:
                return collected_clumpers[0]
            # More than one object found
            elif len(collected_clumpers) > 1:
                # Combine them by concating their dict
                return reduce(lambda a, b: a.concat(b), collected_clumpers)

        return wrapper

    return decorator
