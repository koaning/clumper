# Getting Started

This library offers tools to deal with nested json data structure. To demonstrate how it might work we'll download a dataset locally. It's a list of dictionaries that contains information about pokemon.

```python
import json
import urllib.request

url = 'http://calmcode.io/datasets/pokemon.json'
with urllib.request.urlopen(url) as f:
    pokemon = json.loads(f.read())
```

Here's the first two examples from this list;

```
[{'name': 'Bulbasaur',
  'type': ['Grass', 'Poison'],
  'total': 318,
  'hp': 45,
  'attack': 49},
 {'name': 'Ivysaur',
  'type': ['Grass', 'Poison'],
  'total': 405,
  'hp': 60,
  'attack': 62}]
```

There's about 800 dictionaries in our list which is
big enough to want to not go through manually but also
small enough that we don't need to worry too much
about performance.

### Example

Let's run a basic example.

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

This is the result of this query.

```
[{'name': 'Diglett', 'type': 'Ground', 'ratio': 5.5},
 {'name': 'DeoxysAttack Forme', 'type': 'Psychic', 'ratio': 3.6},
 {'name': 'Krabby', 'type': 'Water', 'ratio': 3.5},
 {'name': 'DeoxysNormal Forme', 'type': 'Psychic', 'ratio': 3.0},
 {'name': 'BanetteMega Banette', 'type': 'Ghost', 'ratio': 2.578125}]
```

Here's what the code did.

0. It imports `Clumper`.
1. It turns the list of pokemon dictionaries into a `Clumper` collection.
2. It removes all the pokemon that have more than 1 type.
3. The dictionaries that are left will have their `type` now as a string instead of a list of strings.
4. These dictionaries will also get a property called `ratio` which is the ratio between `hp` and `attack`.
5. All the keys besides `name`, `type` and `ratio` are removed.
6. The collection is sorted by `ratio`, from high to low.
7. We grab the top 5 after sorting.
8. The results are returned as a list of dictionaries.

## Design

The idea behind the library is that the API is like the English language.
We could say that the dataset is like a **noun** and that each method is like a **verb**.

Each verb will tell the API *what* will needs to happen to the data and the
input to the verb will tell you how *how* this will happen. For example,
the `.keep()` method will filter out data and how it will filter data is
explained by the lambda function that we pass in.

The idea is that most analyses that you'd be interested in doing can be
constructed using just these verbs. You can see a detailed view of how to use all the verbs in the [api description](/api/clumper/).

<small>In case you're interested, this was inspired by the [dplyr library in R](https://dplyr.tidyverse.org/). </small>
