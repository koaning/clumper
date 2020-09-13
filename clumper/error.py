def raise_yaml_dep_error():
    msg = """
    If you want to read yaml files you need to install PyYaml.
    To install, run:

    > python -m pip install clumper[yaml]
    """
    raise RuntimeError(msg)
