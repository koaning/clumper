class Clumper:
    def __init__(self, blob):
        self.blob = blob

    def __len__(self):
        return len(self.blob)

    def keep(self, *funcs):
        data = self.blob
        for func in funcs:
            data = [d for d in data if func(d)]
        return Clumper(data)

    def head(self, n):
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be a positive integer, got {n}")
        n = min(n, len(self))
        return Clumper([self.blob[i] for i in range(n)])

    def tail(self, n):
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be positive, got {n}")
        n = min(n, len(self))
        return Clumper([self.blob[-i] for i in range(len(self) - n, len(self))])

    def select(self, *keys):
        return Clumper([{k: d[k] for k in keys} for d in self.blob])

    def mutate(self, **kwargs):
        data = self.blob
        for key, func in kwargs.items():
            for i in range(len(data)):
                data[i][key] = func(data[i])
        return Clumper(data)

    def sort(self, key, reverse=False):
        return Clumper(sorted(self.blob, key=key, reverse=reverse))

    def collect(self):
        return self.blob
