<img src="theme/logo.png" width=185 height=185 align="right">

# **Clumper**

**A small python library that can clump lists of nested data together.**

Part of a video series on [calmcode.io](https://calmcode.io).

## Base Example

Clumper allows you to quickly parse through a list of json-like data.

Here's an example of such a dataset.

```python
pokemon = [
    {'name': 'Bulbasaur', 'type': ['Grass', 'Poison'], 'hp': 45, 'attack': 49},
    {'name': 'Charmander', 'type': ['Fire'], 'hp': 39, 'attack': 52},
    ...
]
```

Given this list of dictionaries we can write the following query;

```python
from clumper import Clumper

clump = Clumper.read_json('https://calmcode.io/datasets/pokemon.json')

(clump
  .keep(lambda d: len(d['type']) == 1)
  .mutate(type=lambda d: d['type'][0],
          ratio=lambda d: d['attack']/d['hp'])
  .select('name', 'type', 'ratio')
  .sort(lambda d: d['ratio'], reverse=True)
  .head(5)
  .collect())
```

<details>
  <summary><b>What this code does line-by-line.</b></summary>
This code will perform the following steps.

0. It imports `Clumper`.
1. It fetches a list of json-blobs about pokemon from the internet.
2. It removes all the pokemon that have more than 1 type.
3. The dictionaries that are left will have their `type` now as a string instead of a list of strings.
4. The dictionaries that are left will also have a property called `ratio` which calculates the ratio between `hp` and `attack`.
5. All the keys besides `name`, `type` and `ratio` are removed.
6. The collection is sorted by `ratio`, from high to low.
7. We grab the top 5 after sorting.
8. The results are returned as a list of dictionaries.
</details>

This is what we get back:

```python
[{'name': 'Diglett', 'type': 'Ground', 'ratio': 5.5},
 {'name': 'DeoxysAttack Forme', 'type': 'Psychic', 'ratio': 3.6},
 {'name': 'Krabby', 'type': 'Water', 'ratio': 3.5},
 {'name': 'DeoxysNormal Forme', 'type': 'Psychic', 'ratio': 3.0},
 {'name': 'BanetteMega Banette', 'type': 'Ghost', 'ratio': 2.578125}]
```

## Documentation

We've got a lovely [documentation page](https://koaning.github.io/clumper/) that explains how the library works.

[![](docs/img/groupby.png)](https://koaning.github.io/clumper/)

## Features

- This library has no dependencies besides a modern version of python.
- The library offers a pattern of verbs that are very expressive.
- You can write code from top to bottom, left to right.
- You can read in many `json`/`yaml`/`csv` files by using a wildcard `*`.
- MIT License

## Installation

You can install this package via `pip`.

```
pip install clumper
```

It may be safer however to install via;

```
python -m pip install clumper
```

For details on why, check out [this resource](https://calmcode.io/virtualenv/intro.html).

There are some optional dependencies that you might want to install as well.

```
python -m pip install clumper[yaml]
```

## Contributing

Make sure you check out the [issue list](https://github.com/koaning/clumper/issues) beforehand in order
to prevent double work before you make a pull request. To get started locally, you can clone
the repo and quickly get started using the `Makefile`.

```
git clone git@github.com:koaning/clumper.git
cd clumper
make install-dev
```
