import json
import csv
import pathlib
import itertools as it
import urllib.request
from functools import reduce
from statistics import mean, variance, stdev, median


from clumper.error import raise_yaml_dep_error
from clumper.decorators import (
    return_value_if_empty,
    grouped,
    dict_collection_only,
    multifile,
)


class Clumper:
    """
    This object adds methods to a list of dictionaries that make
    it nicer to explore.

    Arguments:
        blob: the list of data to turn into a Clumper
        groups: specify any groups you'd like to attach to the Clumper
        listify: if the input is a dictionary, turn it into a list with one dictionary inside beforehand.

    Usage:

    ```python
    from clumper import Clumper

    list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

    c = Clumper(list_dicts)
    assert len(c) == 4
    ```
    """

    def __init__(self, blob, groups=tuple(), listify=True):
        self.blob = blob.copy()
        if listify:
            if isinstance(blob, dict):
                self.blob = [blob.copy()]
        self.groups = groups

    def __len__(self):
        return 1 if isinstance(self.blob, dict) else len(self.blob)

    def __iter__(self):
        return self.blob.__iter__()

    def __repr__(self):
        return f"<Clumper groups={self.groups} len={len(self)} @{hex(id(self))}>"

    @classmethod
    @multifile()
    def read_csv(
        cls,
        path,
        delimiter=",",
        na_values=None,
        dtype=None,
        fieldnames=None,
        n=None,
        add_path=False,
    ):
        """
        Reads in a csv file. Can also read files from url.

        ![](../img/read_csv.png)

        Arguments:
            path: filename, url, `pathlib.Path` or list of `pathlib.Path`. Filenames can include a wildcard `*`.
            delimiter: Delimiter used in the csv file. Must be a single character and `,` is the default.
            n: Number of rows to read in. Useful when reading large files. If `None`, all rows are read.
            fieldnames: Allows you to set the fieldnames if the header is missing. By default, the first
                        row of the csv will provide the Clumper keys if fieldnames is `None`. If fieldnames
                        is provided, then the first row becomes part of the data. You should ensure that
                        the correct number of fieldnames is supplied, as an incorrect number can lead
                        to an irregular outcome. If the row has seven fields and the number of fields in
                        fieldnames length is 3, then every row will have only 3 values, the remaining four
                        will be lumped into a list, and assigned key `None`. If the rows have fewer fields
                        than fieldnames, then the missing values are filled in with `None`.
            na_values: This provides an option for treating null values. If `ignore`, null values are
                       returned as empty strings (""). If `None`, then for each row, the key,value pair
                       with the null values  will be truncated from the row. The only values treated as
                       null are empty strings("") and "NA".
            add_path: Adds the name of the read path to each item in the Clumper. Is useful when using wildcards to
                      read in multiple files at once.
            dtype: Data type for each value in a key:value pair. If `None`, then values will be read in as strings.
                   Available dtypes are (int, float, str). If a single dtype is passed, then all values will be
                   converted to the data type and raise an error, if not applicable. For different data types for different
                   key, value pairs, a dictionary of {key: data_type} passed to dtype argument will change the value for
                   every key with the data type, and raise an error if not applicable.

        Usage:

        ```python
        from clumper import Clumper

        clump = Clumper.read_csv("tests/data/monopoly.csv")
        assert len(clump) == 22

        clump = Clumper.read_csv("tests/data/monopoly.csv", n = 10)
        assert len(clump) == 10

        clump = Clumper.read_csv("https://calmcode.io/datasets/monopoly.csv")
        assert len(clump) == 22

        # If the fieldnames argument is not None, then the first row becomes part of the data.
        fieldnames = ['date', 'currency', 'country', 'price', 'dollar_rate', 'cost']
        clump = Clumper.read_csv("https://calmcode.io/datasets/bigmac.csv", fieldnames=fieldnames)

        first_row = ['date', 'currency_code','name','local_price', 'dollar_ex', 'dollar_price']
        assert clump.head(1).equals([dict(zip(fieldnames, first_row))])
        ```
        """
        if n is not None:
            if n <= 0:
                raise ValueError("Number of lines to read must be > 0.")

        # conveniently excludes pathlib files here and removes
        # the need to write code to check pathlib files in other places.
        # Quick conversion in case of Path object
        path = str(path)
        if path.startswith(("https:", "http:")):
            with urllib.request.urlopen(path) as resp:
                if fieldnames is None:
                    fieldnames = resp.readline().decode().strip().split(",")
                # This section allows us to chunk the rows, if nrows is supplied.
                body = it.islice(resp, 0, n)
                body = (word.decode().strip().split(",") for word in body)
                body = it.product([fieldnames], body)
                result = [dict(zip(key, values)) for key, values in body]
        else:
            with open(path, newline="") as csvfile:
                reader = csv.DictReader(
                    csvfile, delimiter=delimiter, fieldnames=fieldnames
                )
                # python version less than 3.8 returns an OrderedDict
                result = [dict(entry) for entry in it.islice(reader, 0, n)]

        # Null values, same as missing keys.
        # If there are null values/missing keys, they will be truncated from the dictionary.
        # Python's csv module treats null values as empty strings when writing to a csv -
        # https://docs.python.org/3.8/library/csv.html#csv.DictWriter.
        # The user can choose to explicitly show missing keys/null values in the dictionary,
        # by assigning `ignore` to the na_values argument. At the moment, the default for
        # null values are empty string ("") and "NA".

        if na_values == "ignore":
            result = result
        else:
            na_values = ["", "NA"]
            result = [
                {key: value for key, value in entry.items() if value not in na_values}
                for entry in result
            ]

        # The csv module reads every row as a string, there are no data type assumptions.
        # This function attempts to solve this. The user can pass a string of either
        # ('int', 'str', 'float') or if the user knows the keys/fieldnames, can pass a
        # dictionary mapping the key to the data type.
        # Technically 'str' data type is not needed, since data is read in as strings anyway.

        if not (isinstance(dtype, (dict, str)) or dtype is None):
            raise TypeError(
                """dtype should be a dictionary pair of key and data type, or a single string data type"""
            )

        dtype_mapping = {"int": int, "float": float, "str": str}
        if dtype:
            if isinstance(dtype, str) and dtype in ("int", "float", "str"):
                result = [
                    {key: dtype_mapping[dtype](value) for key, value in entry.items()}
                    for entry in result
                ]
            else:
                result = [
                    {
                        key: dtype_mapping[dtype[key]](value) if key in dtype else value
                        for key, value in entry.items()
                    }
                    for entry in result
                ]

        if add_path:
            return Clumper(result).mutate(read_path=lambda d: path)
        return Clumper(result)

    @classmethod
    @multifile()
    def read_json(cls, path, n=None, listify=True, add_path=False):
        """
        Reads in a json file. Can also read files from url.

        ![](../img/read_json.png)

        Arguments:
            path: filename, url, `pathlib.Path` or list of `pathlib.Path`. Filenames can include a wildcard `*`.
            n: Number of rows to read in. Useful when reading large files. If `None`, all rows are read.
            listify: if the input is a single json dictionary, turn it into a list with that dictionary inside of it
                     before passing it along to the Clumper.
            add_path: Adds the name of the read path to each item in the Clumper. Is useful when using wildcards to
                      read in multiple files at once.

        Usage:

        ```python
        from clumper import Clumper

        clump = Clumper.read_json("tests/data/pokemon.json")
        assert len(clump) == 800

        clump = Clumper.read_json("https://calmcode.io/datasets/got.json")
        assert len(clump) == 30

        clump = Clumper.read_json("https://calmcode.io/datasets/got.json", n=10)
        assert len(clump) == 10
        ```
        """
        if n is not None:
            if n <= 0:
                raise ValueError("Number of lines to read must be > 0.")

        # Quick conversion in case of Path object
        path = str(path)

        if path.startswith("https:") or path.startswith("http:"):
            with urllib.request.urlopen(path) as resp:
                data = json.loads(resp.read())
        else:
            data = json.loads(pathlib.Path(path).read_text())
        if add_path:
            if isinstance(data, dict):
                data["read_path"] = path
            if isinstance(data, list):
                for d in data:
                    d["read_path"] = path
        if n:
            return Clumper(list(it.islice(data, 0, n)))
        return Clumper(data, listify=listify)

    @classmethod
    @multifile()
    def read_jsonl(cls, path, n=None, listify=True, add_path=False):
        """
        Reads in a jsonl file. Can also read files from url.

        ![](../img/read_jsonl.png)

        Arguments:
            path: filename, url, `pathlib.Path` or list of `pathlib.Path`. Filenames can include a wildcard `*`.
            n: Number of rows to read in. Useful when reading large files. If `None`, all rows are read.
            listify: if the input is a single json dictionary, turn it into a list with that dictionary inside of it
                     before passing it along to the Clumper.
            add_path: Adds the name of the filepath to each item in the Clumper. Is useful when using wildcards to
                      read in multiple files at once.

        Usage:

        ```python
        from clumper import Clumper

        clump = Clumper.read_jsonl("tests/data/cards.jsonl")
        assert len(clump) == 4

        clump = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl")
        assert len(clump) == 800

        clump = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl", n=10)
        assert len(clump) == 10
        ```
        """
        if n is not None:
            if n <= 0:
                raise ValueError("Number of lines to read must be > 0.")

        # Quick conversion in case of Path object
        path = str(path)

        # Case 1 : Open cloud file in stream
        if path.startswith("https:") or path.startswith("http:"):
            f = urllib.request.urlopen(path)
        # Case 2 : Local file
        else:
            f = open(path)

        # Initialize a place to store the parsed data as list
        data_array = []
        # Read it, parse and close it
        with f:
            for current_line_nr, json_string in enumerate(f):
                if n is not None and current_line_nr == n:
                    break
                json_object = json.loads(json_string)
                data_array.append(json_object)
        if add_path:
            for d in data_array:
                d["read_path"] = path
        # Return it
        return Clumper(data_array, listify=listify)

    @classmethod
    @multifile()
    def read_yaml(cls, path, n=None, listify=True, add_path=False):
        """
        Reads in a yaml file.

        ![](../img/read_yaml.png)

        Arguments:
            path: filename, url, `pathlib.Path` or list of `pathlib.Path`. Filenames can include a wildcard `*`.
            n: number of lines to read in, if `None` will read all
            listify: if the input is a single json dictionary, turn it into a list with that dictionary inside of it
                     before passing it along to the Clumper.
            add_path: Adds the name of the filepath to each item in the Clumper. Is useful when using wildcards to
                      read in multiple files at once.

        Important:
            This method requires the `PyYAML` dependency which is not installed automatically.
            To install it you can run;

            ```
            # This will only install the yaml dependencies.
            pip install clumper[yaml]
            # This will install all optional dependencies.
            pip install clumper[all]
            ```

        Usage:

        ```python
        from clumper import Clumper

        clump = Clumper.read_yaml("tests/data/demo-flat-1.yaml")
        assert len(clump) == 3

        clump = Clumper.read_yaml("tests/data/demo-flat-*.yaml")
        assert len(clump) == 6
        ```
        """

        # Quick conversion in case of Path object
        path = str(path)

        # Case 1 : Open cloud file in stream
        if path.startswith(("https:", "http:")):
            f = urllib.request.urlopen(path)
        # Case 2 : Local file
        else:
            f = open(path)

        # Try to load it but tell the user to install if not there.
        try:
            import yaml

            data = yaml.load(f.read(), Loader=yaml.FullLoader)
            if isinstance(data, dict):
                if add_path:
                    data["read_path"] = path
                return Clumper(data, listify=listify)
            if add_path:
                for d in data:
                    d["read_path"] = path
            if n:
                return Clumper(list(it.islice(data, 0, n)), listify=listify)
            return Clumper(data, listify=listify)
        except ImportError:
            raise_yaml_dep_error()

    def write_yaml(self, path):
        """
        Write the collection of data as a yaml file.

        Arguments:
            path: path to write the file to

        Important:
            This method requires the `PyYAML` dependency which is not installed automatically.
            To install it you can run;

            ```
            # This will only install the yaml dependencies.
            pip install clumper[yaml]
            # This will install all optional dependencies.
            pip install clumper[all]
            ```

        Usage:

        ```python
        from clumper import Clumper
        clump_orig = Clumper.read_yaml("tests/data/demo-flat-1.yaml")
        clump_orig.write_json("tests/data/demo-flat-copy.json")

        clump_copy = Clumper.read_json("tests/data/demo-flat-copy.json")
        assert clump_copy.collect() == clump_orig.collect()
        ```
        """
        try:
            import yaml

            with open(path, "x") as f:
                txt = yaml.dump(self.collect())
                f.write(txt)
        except ImportError:
            raise_yaml_dep_error()

    def write_json(self, path, sort_keys=False, indent=None):
        """
        Writes to a json file.

        Arguments:
            path: filename
            sort_keys: If sort_keys is true (default: False), then the output of dictionaries will be sorted by key.
            indent: If indent is a non-negative integer (default: None), then JSON array elements members will be pretty-printed with that indent level.

        Usage:

        ```python
        from clumper import Clumper
        clump_orig = Clumper.read_json("tests/data/pokemon.json")
        clump_orig.write_json("tests/data/pokemon_copy.json")

        clump_copy = Clumper.read_json("tests/data/pokemon_copy.json")
        assert clump_copy.collect() == clump_orig.collect()
        ```
        """
        # Create a new file and open it for writing
        with open(path, "w") as f:
            json.dump(self.collect(), f, sort_keys=sort_keys, indent=indent)

    def write_jsonl(self, path, sort_keys=False, indent=None):
        """
        Writes to a jsonl file.

        Arguments:
            path: filename
            sort_keys: If sort_keys is true (default: False), then the output of dictionaries will be sorted by key.
            indent: If indent is a non-negative integer (default: None), then JSON array elements members will be pretty-printed with that indent level.
        """
        # Create a new file and open it for writing
        with open(path, "x") as f:
            for current_line_nr, json_dict in enumerate(self.collect()):
                f.write(
                    json.dumps(json_dict, sort_keys=sort_keys, indent=indent) + "\n"
                )

    def write_csv(self, path, mode="w"):
        """
        Write to a csv file.

        Arguments:
        path: filename
        mode: `w` writes to a file if it does not exist, or overwrites if it already exists,
               while `a`: - append to file if it already exists. The default is `w`.

        Note that null values will be exported as empty strings; this is the convention chosen by Python.

        Usage:

        ```python
        from clumper import Clumper
        from pathlib import Path
        path = '/tmp/monopoly.csv'
        Clumper.read_csv("tests/data/monopoly.csv").write_csv(path)
        reader = Clumper.read_csv(path)
        assert Clumper.read_csv("tests/data/monopoly.csv").collect() == reader.collect()
        ```
        """

        with open(path, mode=mode, newline="") as csvfile:
            fieldnames = self.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for row in self:
                writer.writerow(row)

    def _create_new(self, blob):
        """
        Creates a new collection of data while preserving settings of the
        current collection (most notably, `groups`).
        """
        return Clumper(blob, groups=self.groups)

    def group_by(self, *cols):
        """
        Sets a group on this clumper object or overrides a previous setting.
        A group will affect how some verbs behave. You can undo this behavior
        with `.ungroup()`.

        ![](../img/groupby.png)

        ```python
        from clumper import Clumper

        clump = Clumper([{"a": 1}]).group_by("a")
        assert clump.groups == ("a", )
        ```
        """
        self.groups = cols
        return self

    def ungroup(self):
        """
        Removes all grouping from the collection.

        ![](../img/ungroup.png)

        ```python
        from clumper import Clumper

        clump = Clumper([{"a": 1}]).group_by("a")
        assert clump.groups == ("a", )
        assert clump.ungroup().groups == tuple()
        ```
        """
        self.groups = tuple()
        return self

    @grouped
    @dict_collection_only
    def transform(self, **kwargs):
        """
        Does an aggregation just like `.agg()` however instead of reducing the rows we
        merge the results back with the original data. This saves a lot of compute time
        because effectively this prevents us from performing a join.

        ![](../img/transform-with-groups.png)

        Arguments:
            kwargs: keyword arguments that represent the aggregation that is about to happen, see usage below.

        Warning:
            This method is aware of groups. There may be different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        data = [
            {"a": 6, "grp": "a"},
            {"a": 2, "grp": "b"},
            {"a": 7, "grp": "a"},
            {"a": 9, "grp": "b"},
            {"a": 5, "grp": "a"}
        ]

        tfm_clump = (Clumper(data)
                      .group_by("grp")
                      .transform(s=("a", "sum"),
                                 u=("a", "unique")))

        expected = [
            {'a': 6, 'grp': 'a', 's': 18, 'u': [5, 6, 7]},
            {'a': 7, 'grp': 'a', 's': 18, 'u': [5, 6, 7]},
            {'a': 5, 'grp': 'a', 's': 18, 'u': [5, 6, 7]},
            {'a': 2, 'grp': 'b', 's': 11, 'u': [9, 2]},
            {'a': 9, 'grp': 'b', 's': 11, 'u': [9, 2]}
        ]

        assert tfm_clump.equals(expected)
        ```
        """
        agg_results = self.agg(**kwargs)
        return self.left_join(agg_results, mapping={k: k for k in self.groups})

    def equals(self, data):
        """
        Compares the collection of items with a list. Returns `True` if they have the same contents.
        Note that we do not care about the order of the elements.

        This method is used internally for testing but it can also be very useful for bug reporting.

        ![](../img/equals.png)

        Arguments:
            data: a list of that to compare against

        Usage:

        ```python
        from clumper import Clumper

        data = [{"a": 1}]
        clump = Clumper(data)
        assert clump.equals(data)
        assert not clump.equals([{"b":1}])
        ```
        """
        for i in self:
            if i not in data:
                return False
        for i in data:
            if i not in self:
                return False
        return True

    def drop_duplicates(self):
        """
        Iterates over all elements to remove duplicates.

        ![](../img/drop_duplicates.png)

        Usage:

        ```python
        from clumper import Clumper

        data = [{"a": 1}, {"a": 2}, {"a": 2}]
        clump = Clumper(data).drop_duplicates()
        expected = [{"a": 1}, {"a": 2}]
        assert clump.equals(expected)
        ```
        """
        uniques = []
        for d in self:
            if d not in uniques:
                uniques.append(d)
        return self._create_new(uniques)

    @staticmethod
    def _merge_dicts(d1, d2, mapping, suffix1, suffix2):
        """
        Merge two dictionaries together. Keeping suffixes in mind.
        """
        map_keys = list(mapping.keys()) + list(mapping.values())
        keys_to_suffix = [
            k for k in set(d1.keys()).intersection(set(d2.keys())) if k not in map_keys
        ]
        d1_new = {(k + suffix1 if k in keys_to_suffix else k): v for k, v in d1.items()}
        d2_new = {(k + suffix2 if k in keys_to_suffix else k): v for k, v in d2.items()}
        return {**d1_new, **d2_new}

    @dict_collection_only
    def left_join(self, other, mapping, lsuffix="", rsuffix="_joined"):
        """
        Performs a left join on two collections.

        Each item from the left set will appear in the final collection. Only
        some items from the right set may appear if a merge is possible. There
        may be multiple copies of the left set if it can be joined multiple times.

        ![](../img/left_join.png)

        Arguments:
            other: another collection to join with
            mapping: a dictionary of **left-keys**:**right-keys** that explain how to join
            lsuffix: a suffix to add to the left keys in case of an overlap
            rsuffix: a suffix to add to the right keys in case of an overlap

        Usage:

        ```python
        from clumper import Clumper

        left = Clumper([
            {"a": 1, "b": 4},
            {"a": 2, "b": 6},
            {"a": 3, "b": 8},
        ])

        right = Clumper([
            {"c": 9, "b": 4},
            {"c": 8, "b": 5},
            {"c": 7, "b": 6},
        ])

        result = left.left_join(right, mapping={"b": "b"})
        expected = [
            {"a": 1, "b": 4, "c": 9},
            {"a": 2, "b": 6, "c": 7},
            {"a": 3, "b": 8},
        ]

        assert result.equals(expected)
        ```
        """
        result = []
        # This is a naive implementation. Speedup seems possible.
        for d_i in self:
            values_i = [d_i[k] for k in mapping.keys() if k in d_i.keys()]
            d_i_added = False
            for d_j in other:
                values_j = [d_j[k] for k in mapping.values() if k in d_j.keys()]
                if len(mapping) == len(values_i) == len(values_j):
                    if values_i == values_j:
                        result.append(
                            Clumper._merge_dicts(d_i, d_j, mapping, lsuffix, rsuffix)
                        )
                        d_i_added = True
            if not d_i_added:
                result.append(d_i)
        return self._create_new(result)

    @dict_collection_only
    def inner_join(self, other, mapping, lsuffix="", rsuffix="_joined"):
        """
        Performs an inner join on two collections.

        ![](../img/inner_join.png)

        Arguments:
            other: another collection to join with
            mapping: a dictionary of **left-keys**:**right-keys** that explain how to join
            lsuffix: a suffix to add to the left keys in case of an overlap
            rsuffix: a suffix to add to the right keys in case of an overlap

        Usage:

        ```python
        from clumper import Clumper

        left = Clumper([
            {"a": 1, "b":4},
            {"a": 2, "b":6},
            {"a": 3, "b":8},
        ])

        right = Clumper([
            {"c": 9, "b":4},
            {"c": 8, "b":5},
            {"c": 7, "b":6},
        ])

        result = left.inner_join(right, mapping={"b": "b"})
        expected = [
            {"a": 1, "b": 4, "c": 9},
            {"a": 2, "b": 6, "c": 7},
        ]

        assert result.equals(expected)
        ```
        """
        result = []
        # This is a naive implementation. Speedup seems possible.
        for d_i in self:
            values_i = [d_i[k] for k in mapping.keys() if k in d_i.keys()]
            for d_j in other:
                values_j = [d_j[k] for k in mapping.values() if k in d_j.keys()]
                if len(mapping) == len(values_i) == len(values_j):
                    if values_i == values_j:
                        result.append(
                            Clumper._merge_dicts(d_i, d_j, mapping, lsuffix, rsuffix)
                        )
        return self._create_new(result)

    @property
    def only_has_dictionaries(self):
        return all([isinstance(d, dict) for d in self])

    @dict_collection_only
    @grouped
    def agg(self, **kwargs):
        """
        Does an aggregation on a collection of dictionaries. If there are no groups active
        then this method will create a single dictionary containing a summary. If there are
        groups active then the dataset will first split up, then apply the summaries after
        which everything is combined again into a single collection.

        When defining a summary to apply you'll need to pass three things:

        1. the name of the new key
        2. the key you'd like to summarise (first item in the tuple)
        3. the summary you'd like to calculate on that key (second item in the tuple)

        It can also accept a string and it will try to fetch an appropriate function
        for you. If you pass a string it must be either: `mean`, `count`, `unique`,
        `n_unique`, `sum`, `min`, `max`, `median`, `values`, `var`, `std`, `first` or `last`.

        ![](../img/split-apply-combine.png)

        Warning:
            This method is aware of groups. There may be different results if a group is active.

        Arguments:
            kwargs: keyword arguments that represent the aggregation that is about to happen, see usage below.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3},
            {'a': 3}
        ]

        (Clumper(list_dicts)
          .agg(mean_a=('a', 'mean'),
               min_b=('b', 'min'),
               max_b=('b', 'max'))
          .collect())

        another_list_dicts = [
            {'a': 1, 'c': 'a'},
            {'a': 2, 'c': 'b'},
            {'a': 3, 'c': 'a'}
        ]

        (Clumper(another_list_dicts)
          .group_by('c')
          .agg(mean_a=('a', 'mean'),
               uniq_a=('a', 'unique'))
          .collect())
        ```

        Advanced Usage:

        You can also supply this verb your own functions if you'd like.

        ```python
        from clumper import Clumper

        data = [
            {"a": 7, "grp": "a"},
            {"a": 2, "grp": "b"},
            {"a": 7, "grp": "a"},
            {"a": 9, "grp": "b"},
            {"a": 5, "grp": "a"}
        ]

        tfm_clump = (Clumper(data)
                        .group_by("grp")
                        .transform(s=("a", sum),
                                    u=("a", lambda x: set(x))))

        expected = [
            {'a': 7, 'grp': 'a', 's': 19, 'u': {5, 7}},
            {'a': 7, 'grp': 'a', 's': 19, 'u': {5, 7}},
            {'a': 5, 'grp': 'a', 's': 19, 'u': {5, 7}},
            {'a': 2, 'grp': 'b', 's': 11, 'u': {2, 9}},
            {'a': 9, 'grp': 'b', 's': 11, 'u': {2, 9}}
        ]

        assert tfm_clump.equals(expected)
        ```
        """
        res = {
            name: self.summarise_col(func_str, col)
            for name, (col, func_str) in kwargs.items()
        }
        return Clumper([res], groups=self.groups)

    @dict_collection_only
    def _subsets(self):
        """
        Subsets the data into groups, specified by `.group_by()`.
        Only subsets that have length > 0 are returned.
        """
        result = []
        for gc in self._group_combos():
            subset = self.copy()
            for key, value in gc.items():
                subset = subset.keep(lambda d: d[key] == value)
            if len(subset) > 0:
                result.append(subset)
        return result

    def concat(self, *other):
        """
        Concatenate two or more `Clumper` objects together.

        ![](../img/concat.png)

        ```python
        from clumper import Clumper

        c1 = Clumper([{"a": 1}])
        c2 = Clumper([{"a": 2}])
        c3 = Clumper([{"a": 3}])

        assert len(c1.concat(c2)) == 2
        assert len(c1.concat(c2, c3)) == 3
        assert len(c1.concat(c2).concat(c3)) == 3
        ```
        """

        data = reduce(lambda a, b: a + b, [o.blob for o in other])
        return self._create_new(self.blob + data)

    def _group_combos(self):
        """
        Returns a dictionary of group-value/clumper pairs.
        """
        combinations = [
            comb for comb in it.product(*[self.unique(c) for c in self.groups])
        ]
        return [{k: v for k, v in zip(self.groups, comb)} for comb in combinations]

    def keep(self, *funcs):
        """
        Allows you to select which items to keep and which items to remove.

        ![](../img/keep.png)

        Arguments:
            funcs: functions that indicate which items to keep

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        clump = Clumper(list_dicts).keep(lambda d: d['a'] >= 3)
        expected = [{'a': 3}, {'a': 4}]
        assert clump.equals(expected)
        ```
        """
        data = self.blob.copy()
        for func in funcs:
            data = [d for d in data if func(d)]
        return self._create_new(data)

    def head(self, n=5):
        """
        Selects the top `n` items from the collection.

        ![](../img/head.png)

        Arguments:
            n: the number of items to grab

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        result = Clumper(list_dicts).head(2)
        expected = [{'a': 1}, {'a': 2}]

        assert result.equals(expected)
        ```
        """
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be a positive integer, got {n}")
        n = min(n, len(self))
        return self._create_new([self.blob[i] for i in range(n)])

    def tail(self, n=5):
        """
        Selects the bottom `n` items from the collection.

        ![](../img/tail.png)

        Arguments:
            n: the number of items to grab

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]

        result = Clumper(list_dicts).tail(2)
        expected = [{'a': 3}, {'a': 4}]
        assert result.equals(expected)
        ```
        """
        if not isinstance(n, int):
            raise ValueError(f"`n` must be a positive integer, got {n}")
        if n < 0:
            raise ValueError(f"`n` must be positive, got {n}")
        n = min(n, len(self))
        return self._create_new(self.blob[len(self) - n : len(self)])

    @dict_collection_only
    def unpack(self, name):
        """
        Unpacks a nested list of dictionaries.

        ![](../img/unpack.png)

        Arguments:
            name: the name of the column to unpack

        ```python
        from clumper import Clumper

        list_dicts = {
            'a': 1,
            'rows': [{'b': 2, 'c': 3}, {'b': 3}, {'b': 4}]
        }

        result = Clumper(list_dicts).unpack('rows').collect()

        expected = [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 3},
            {'a': 1, 'b': 4}
        ]

        assert result == expected
        ```
        """
        new_blob = []
        for row in self:
            for d in row[name]:
                new = {k: v for k, v in row.items() if k != name}
                new_blob.append({**new, **d})
        return self._create_new(new_blob)

    @dict_collection_only
    def select(self, *keys):
        """
        Selects a subset of the keys in each item in the collection.

        ![](../img/select.png)

        Arguments:
            keys: the keys to keep

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        clump = Clumper(list_dicts).select('a', 'b')
        assert all(["c" not in d.keys() for d in clump])
        ```
        """
        return self._create_new([{k: d[k] for k in keys} for d in self.blob])

    @dict_collection_only
    def drop(self, *keys):
        """
        Removes a subset of keys from each item in the collection.

        ![](../img/drop.png)

        Arguments:
            keys: the keys to remove

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        clump = Clumper(list_dicts).drop('c')
        assert all(["c" not in d.keys() for d in clump])
        ```
        """
        return self._create_new(
            [{k: v for k, v in d.items() if k not in keys} for d in self.blob]
        )

    @grouped
    def mutate(self, **kwargs):
        """
        Adds or overrides key-value pairs in the collection of dictionaries.

        ![](../img/mutate.png)

        Arguments:
            kwargs: keyword arguments of keyname/function-pairs

        Warning:
            This method is aware of groups. There may be different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3, 'c':4},
            {'a': 1, 'b': 6}]

        result = (Clumper(list_dicts)
                  .mutate(c=lambda d: d['a'] + d['b'],
                          s=lambda d: d['a'] + d['b'] + d['c']))

        expected = [
            {'a': 1, 'b': 2, 'c': 3, 's': 6},
            {'a': 2, 'b': 3, 'c': 5, 's': 10},
            {'a': 1, 'b': 6, 'c': 7, 's': 14}
        ]

        assert result.equals(expected)
        ```
        """
        data = []
        for d in self.blob.copy():
            new = {k: v for k, v in d.items()}
            for key, func in kwargs.items():
                new[key] = func(new)
            data.append(new)
        return self._create_new(data)

    @grouped
    def sort(self, key, reverse=False):
        """
        Allows you to sort the collection of dictionaries.

        ![](../img/sort.png)

        Arguments:
            key: the number of items to grab
            reverse: the number of items to grab

        Warning:
            This method is aware of groups. Expect different results if a group is active.

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 3},
            {'a': 2, 'b': 1}]

        (Clumper(list_dicts)
          .sort(lambda d: d['a'])
          .collect())

        (Clumper(list_dicts)
          .sort(lambda d: d['b'], reverse=True)
          .collect())
        ```
        """
        return self._create_new(sorted(self.blob, key=key, reverse=reverse))

    def map(self, func):
        """
        Directly map one item to another one using a function.
        If you're dealing with dictionaries, consider using
        `mutate` instead.

        ![](../img/map.png)

        Arguments:
            func: the function that will map each item

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': 1}, {'a': 2}]

        (Clumper(list_dicts)
          .map(lambda d: {'a': d['a'], 'b': 1})
          .collect())
        ```
        """
        return self._create_new([func(d) for d in self.blob])

    @dict_collection_only
    def keys(self, overlap=False):
        """
        Returns all the keys of all the items in the collection.

        ![](../img/keys.png)

        Arguments:
            overlap: if `True` only return the keys that overlap in each set

        Usage:

        ```python
        from clumper import Clumper

        data = [{'a': 1, 'b': 2}, {'a': 2, 'c': 3}]

        assert set(Clumper(data).keys(overlap=True)) == {'a'}
        assert set(Clumper(data).keys(overlap=False)) == {'a', 'b', 'c'}
        ```
        """
        if overlap:
            all_keys = [set(d.keys()) for d in self]
            return list(reduce(lambda a, b: a.intersection(b), all_keys))
        return list({k for d in self for k in d.keys()})

    @dict_collection_only
    def explode(self, *to_explode, **kwargs):
        """
        Turns a list in an item into multiple items. The opposite of `.implode()`.

        ![](../img/explode.png)

        Arguments:
            to_explode: keys to explode, will keep the same name
            kwargs: (new name, keys to explode)-pairs

        Usage:

        ```python
        from clumper import Clumper

        data = [{'a': 1, 'items': [1, 2]}]

        clumper = Clumper(data).explode("items")
        expected = [{'a': 1, 'items': 1}, {'a': 1, 'items': 2}]
        assert clumper.equals(expected)

        clumper = Clumper(data).explode(item="items")
        expected = [{'a': 1, 'item': 1}, {'a': 1, 'item': 2}]
        assert clumper.equals(expected)
        ```
        """
        # you can keep the same name by just using *args or overwrite using **kwargs
        kwargs = {**kwargs, **{k: k for k in to_explode}}
        new_name, to_explode = kwargs.keys(), kwargs.values()

        res = []
        for d in self.blob:
            combinations = it.product(*[d[v] for v in to_explode])
            for comb in combinations:
                new_dict = d.copy()
                for k, v in zip(new_name, comb):
                    new_dict[k] = v
                res.append(new_dict)
        return self._create_new(res).drop(*[k for k in to_explode if k not in new_name])

    def rename(self, **kwargs):
        """
        Rename items in the collection.

        Usage:

        ```python
        from clumper import Clumper

        data = [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}]

        clumper = Clumper(data).rename(c="b")
        expected = [{'a': 1, 'c': 3}, {'a': 2, 'c': 4}]
        assert clumper.equals(expected)
        ```
        """
        result = self.copy()
        for new_name, old_name in kwargs.items():
            result = result.mutate(**{new_name: lambda d: d[old_name]}).drop(old_name)
        return result

    def implode(self, **kwargs):
        if len(kwargs) == 0:
            raise ValueError("The `implode` method received no input.")
        return (
            self.transform(**{k: (v, "values") for k, v in kwargs.items()})
            .drop(*kwargs.values())
            .drop_duplicates()
        )

    @property
    def shape(self):
        return len(self), len(self.keys())

    def reduce(self, **kwargs):
        """
        Reduce the collection using reducing functions.

        ![](../img/reduce.png)

        Arguments:
            kwargs: key-function pairs

        Usage:

        ```python
        from clumper import Clumper

        list_ints = [1, 2, 3, 4, 5]

        (Clumper(list_ints)
          .reduce(sum_a = lambda x,y: x + y,
                  min_a = lambda x,y: min(x, y),
                  max_a = lambda x,y: max(x, y))
          .collect())
        ```
        """
        return self._create_new(
            [{k: reduce(func, [b for b in self.blob]) for k, func in kwargs.items()}]
        )

    def pipe(self, func, *args, **kwargs):
        """
        Applies a function to the `Clumper` object in a chain-able manner.

        ![](../img/pipe.png)

        Arguments:
            func: function to apply
            args: arguments that will be passed to the function
            kwargs: keyword-arguments that will be passed to the function

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': i} for i in range(100)]

        def remove_outliers(clump, min_a, max_a):
            return (clump
                      .keep(lambda d: d['a'] >= min_a,
                            lambda d: d['a'] <= max_a))

        result = Clumper(list_dicts).pipe(remove_outliers, min_a=10, max_a=90)
        assert len(result) == 81
        ```
        """
        return func(self, *args, **kwargs)

    def collect(self):
        """
        Returns a list instead of a `Clumper` object.

        ![](../img/collect.png)
        """
        return self.blob

    def copy(self):
        """
        Makes a copy of the collection.

        ![](../img/copy.png)

        Usage:

        ```python
        from clumper import Clumper

        list_dicts = [{'a': i} for i in range(100)]

        c1 = Clumper(list_dicts)
        c2 = c1.copy()
        assert id(c1) != id(c2)
        ```
        """
        return self._create_new([d for d in self.blob])

    def flatten_keys(self, keyname="key"):
        """
        Flattens the keys in the data. Useful when `Clumper` is created with a single large dictionary.

        ![](../img/flatten_keys.png)

        Arguments:
            keyname: the name of the new key

        Usage:

        ```python
        from clumper import Clumper

        data = {
          'feature_1': {'propery_1': 1, 'property_2': 2},
          'feature_2': {'propery_1': 3, 'property_2': 4},
          'feature_3': {'propery_1': 5, 'property_2': 6},
        }

        expected = [
            {'propery_1': 1, 'property_2': 2, 'key': 'feature_1'},
            {'propery_1': 3, 'property_2': 4, 'key': 'feature_2'},
            {'propery_1': 5, 'property_2': 6, 'key': 'feature_3'}
        ]

        assert Clumper(data, listify=False).flatten_keys().collect() == expected
        ```
        """
        return self._create_new([{**v, keyname: k} for k, v in self.blob.items()])

    def show(self, n=1, name=None):
        """
        Prints the first `n` items in the clumper as an example. Very useful for debugging!

        This method requires [rich](https://github.com/willmcgugan/rich) if you want the pretty output.

        ```python
        from clumper import Clumper

        data = [{"n": 123, "data": [1, 2, 3], "maintainer": "Vincent"}]
        Clumper(data).show(n=1, name="Before").explode("data").show(n=3, name="After")
        ```

        ![](../img/show.png)
        """
        try:
            from rich import print as rich_print
            from rich.panel import Panel
            from rich.pretty import Pretty

            item = self.head(n).collect()
            title = f"Clumper len={len(self)}"
            if len(self.groups) > 0:
                title = f"Clumper groups={self.groups} len={len(self)}"
            rich_print(Panel(Pretty(item), title=f"{name}: {title}" if name else ""))
        except ImportError:
            import pprint

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.head(n).collect())
        return self

    def summarise_col(self, func, key):
        """
        Apply your own summary function to a key in the collection.

        It can also accept a string and it will try to fetch an appropriate function
        for you. If you pass a string it must be either: `mean`, `count`, `unique`,
        `n_unique`, `sum`, `min`, `max`, `median`, `values`, `var`, `std`, `first` or `last`.

        Note that this method **ignores groups**. It also does not return a `Clumper`
        collection.

        Usage:

        ```python
        from clumper import Clumper

        clump = Clumper([{"a": 1}, {"a": 2}, {"a": 3}])

        assert clump.summarise_col("last", "a") == 3
        assert clump.summarise_col(lambda d: d[-1], "a") == 3
        ```
        """
        funcs = {
            "mean": mean,
            "count": lambda d: len(d),
            "unique": lambda d: list(set(d)),
            "n_unique": lambda d: len(set(d)),
            "sum": sum,
            "min": min,
            "max": max,
            "median": median,
            "var": variance,
            "std": stdev,
            "values": lambda d: d,
            "first": lambda d: d[0],
            "last": lambda d: d[-1],
        }
        if isinstance(func, str):
            if func not in funcs.keys():
                raise ValueError(
                    f"Passed `func` must be in {funcs.keys()}, got {func}."
                )
            func = funcs[func]
        array = [d[key] for d in self if key in d.keys()]
        return func(array)

    @dict_collection_only
    @return_value_if_empty(value=None)
    def sum(self, col):
        """
        Give the sum of the values that belong to a key.

        ![](../img/sum.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        Clumper(list_of_dicts).sum("a")
        Clumper(list_of_dicts).sum("b")
        ```
        """
        return self.summarise_col("sum", col)

    @dict_collection_only
    @return_value_if_empty(value=None)
    def mean(self, col):
        """
        Give the mean of the values that belong to a key.

        ![](../img/mean.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert round(Clumper(list_of_dicts).mean("a"), 1) == 3.5
        assert round(Clumper(list_of_dicts).mean("b"), 1) == 6.7
        ```
        """
        return self.summarise_col("mean", col)

    @dict_collection_only
    @return_value_if_empty(value=0)
    def count(self, col):
        """
        Counts how often a key appears in the collection.

        ![](../img/count.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert Clumper(list_of_dicts).count("a") == 4
        assert Clumper(list_of_dicts).count("b") == 3
        ```
        """
        return self.summarise_col("count", col)

    @dict_collection_only
    @return_value_if_empty(value=0)
    def n_unique(self, col):
        """
        Returns number of unique values that a key has.

        ![](../img/nunique.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert Clumper(list_of_dicts).n_unique("a") == 3
        assert Clumper(list_of_dicts).n_unique("b") == 2
        ```
        """
        return self.summarise_col("n_unique", col)

    @dict_collection_only
    @return_value_if_empty(value=None)
    def min(self, col):
        """
        Returns minimum value that a key has.

        ![](../img/min.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert Clumper(list_of_dicts).min("a") == 2
        assert Clumper(list_of_dicts).min("b") == 6
        ```
        """
        return self.summarise_col("min", col)

    @dict_collection_only
    @return_value_if_empty(value=None)
    def max(self, col):
        """
        Returns maximum value that a key has.

        ![](../img/max.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert Clumper(list_of_dicts).max("a") == 7
        assert Clumper(list_of_dicts).max("b") == 7
        ```
        """
        return self.summarise_col("max", col)

    @dict_collection_only
    @return_value_if_empty(value=[])
    def unique(self, col):
        """
        Returns a set of unique values that a key has.

        ![](../img/unique.png)

        Usage:

        ```python
        from clumper import Clumper

        list_of_dicts = [
            {'a': 7},
            {'a': 2, 'b': 7},
            {'a': 3, 'b': 6},
            {'a': 2, 'b': 7}
        ]

        assert Clumper(list_of_dicts).unique("a") == [2, 3, 7]
        assert Clumper(list_of_dicts).unique("b") == [6, 7]
        ```
        """
        return self.summarise_col("unique", col)
