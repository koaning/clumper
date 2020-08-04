class _underscore:
    """
    This is a hacky feature still in active development.
    """

    def __init__(self, str_repr="_"):
        self.str_repr = str_repr

    def clean_str(self, n):
        return f'"{n}"' if isinstance(n, str) else n

    def __call__(self, _):
        return eval(self.str_repr)

    def __add__(self, n):
        str_repr = f"({self.str_repr}) + {n}"
        return _underscore(str_repr=str_repr)

    def __sub__(self, n):
        str_repr = f"({self.str_repr}) - {n}"
        return _underscore(str_repr=str_repr)

    def __mul__(self, n):
        str_repr = f"({self.str_repr}) * {n}"
        return _underscore(str_repr=str_repr)

    def __mod__(self, n):
        str_repr = f"({self.str_repr}) % {n}"
        return _underscore(str_repr=str_repr)

    def __eq__(self, n):
        str_repr = f"({self.str_repr}) == {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __ne__(self, n):
        str_repr = f"({self.str_repr}) != {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __ge__(self, n):
        str_repr = f"({self.str_repr}) >= {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __gt__(self, n):
        str_repr = f"({self.str_repr}) > {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __le__(self, n):
        str_repr = f"({self.str_repr}) <= {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __lt__(self, n):
        str_repr = f"({self.str_repr}) < {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __getitem__(self, n):
        str_repr = f"({self.str_repr})[{self.clean_str(n)}]"
        return _underscore(str_repr=str_repr)

    def __truediv__(self, n):
        str_repr = f"({self.str_repr}) / {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __floordiv__(self, n):
        str_repr = f"({self.str_repr}) // {self.clean_str(n)}"
        return _underscore(str_repr=str_repr)

    def __abs__(self, n):
        str_repr = f"abs({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __int__(self, n):
        str_repr = f"int({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __float__(self, n):
        str_repr = f"float({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __round__(self, n):
        str_repr = f"round({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __ceil__(self, n):
        str_repr = f"ceil({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __floor__(self, n):
        str_repr = f"floor({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __trunc__(self, n):
        str_repr = f"trunc({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __len__(self, n):
        str_repr = f"len({self.str_repr})"
        return _underscore(str_repr=str_repr)

    def __setitem__(self, k, v):
        str_repr = f"setattr({self.str_repr}, {k}, {v})"
        return _underscore(str_repr=str_repr)

    def __repr__(self):
        return f"<func: {self.str_repr}>"


_ = _underscore()
