def mean(colname, blob):
    s = sum([d[colname] for d in blob if colname in d.keys()])
    return s / len(blob)


def count(colname, blob):
    return sum([1 for d in blob if colname in d.keys()])


def n_unique(colname, blob):
    return sum({d[colname] for d in blob if colname in d.keys()})


def minimum(colname, blob):
    return min([d[colname] for d in blob if colname in d.keys()])


def maximum(colname, blob):
    return max({d[colname] for d in blob if colname in d.keys()})


agg = {
    "mean": mean,
    "count": count,
    "n_unique": n_unique,
    "max": maximum,
    "min": minimum,
}
