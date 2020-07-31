<img src="theme/logo.png" width=185 height=185 align="right">

# **Clumper**

**A small python library that can clump lists of data together.**

Part of a video series on [calmcode.io](https://calmcode.io).

# Alpha Notice

This package is really new and not a whole lot of users have
been able to find *all* the edge cases yet.

## Base Example

Clumper allows you to quickly parse through a list of json-like data.

Here's an example of such a dataset.

```python
pokemon = [
    {'name': 'Bulbasaur', 'type': ['Grass', 'Poison'], 'hp': 45, 'attack': 49}
    {'name': 'Charmander', 'type': ['Fire'], 'hp': 39, 'attack': 52},
    ...
]
```

<details>
  <summary><b>Download this dataset.</b></summary>
You can fetch the dataset by from the commandline.

<pre style="padding: 8px">
wget https://calmcode.io/datasets/pokemon.json
</pre>

You can fetch the dataset by from python.

<pre style="padding: 8px" lang="python">
import json
import urllib.request <br>
url = 'http://calmcode.io/datasets/pokemon.json'
with urllib.request.urlopen(url) as f:
    pokemon = json.loads(f.read())
</pre>


You can also download it manually [here](https://calmcode.io/datasets.html).
</details>

Given this list of dictionaries we can write the following query;

```python
from clumper import Clumper

(Clumper(pokemon)
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
1. It turns the list of pokemon dictionaries into a `Clumper`.
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


## Contributing

Make sure you check out the [issue list](https://github.com/koaning/clumper/issues) beforehand in order
to prevent double work before you make a pull request. To get started locally, you can clone
the repo and quickly get started using the `Makefile`.

```
git clone git@github.com:koaning/clumper.git
cd clumper
make install-dev
```
