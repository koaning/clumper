We'll demonstrate a task using some data from game of thrones.
The data was originally retreived via [an api of fire and ice](https://www.anapioficeandfire.com).

## Fetching Data

This library has a class method that allows you to read json. This can be data from disk, or
a web url. We'll download the data and have a quick look at the contents.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")
clump.head(1).collect()
```

This yields:

```python
[{'url': ['https://www.anapioficeandfire.com/api/characters/1022'],
  'id': [1022],
  'name': ['Theon Greyjoy'],
  'gender': ['Male'],
  'culture': ['Ironborn'],
  'born': ['In 278 AC or 279 AC, at Pyke'],
  'died': [''],
  'alive': [True],
  'titles': ['Prince of Winterfell',
   'Captain of Sea Bitch',
   'Lord of the Iron Islands (by law of the green lands)'],
  'aliases': ['Prince of Fools', 'Theon Turncloak', 'Reek', 'Theon Kinslayer'],
  'father': [''],
  'mother': [''],
  'spouse': [''],
  'allegiances': ['House Greyjoy of Pyke'],
  'books': ['A Game of Thrones', 'A Storm of Swords', 'A Feast for Crows'],
  'povBooks': ['A Clash of Kings', 'A Dance with Dragons'],
  'tvSeries': ['Season 1',
   'Season 2',
   'Season 3',
   'Season 4',
   'Season 5',
   'Season 6'],
  'playedBy': ['Alfie Allen']}]
```

This is just a single element and we can see that there is a nested datastructure here.

The goal of this example is to reshape the data. We want a dictionary per `tvSeries` that
has a list of all the characters that played in that season.

## Less Data

Let's start by making the data just a bit simpler. We're only interested in the `name` and
`tvSeries` keys.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")

(clump
  .select('name', 'tvSeries')
  .head(3)
  .collect())
```

This yields:

```python
[{'name': ['Theon Greyjoy'],
  'tvSeries': ['Season 1',
   'Season 2',
   'Season 3',
   'Season 4',
   'Season 5',
   'Season 6']},
 {'name': ['Tyrion Lannister'],
  'tvSeries': ['Season 1',
   'Season 2',
   'Season 3',
   'Season 4',
   'Season 5',
   'Season 6']},
 {'name': ['Victarion Greyjoy'], 'tvSeries': ['']}]
```

That's a whole lot less data to worry about. That's nice.

We now have two keys that are nested. Let's unlist both.

## Explode

We can use `.explode()` here to explode each key here independantly.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")

(clump
  .select('name', 'tvSeries')
  .explode('name', 'tvSeries')
  .head(15)
  .collect())
```

This yields:

```python
[{'name': 'Theon Greyjoy', 'tvSeries': 'Season 1'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 2'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 3'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 4'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 5'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 6'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 1'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 2'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 3'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 4'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 5'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 6'},
 {'name': 'Victarion Greyjoy', 'tvSeries': ''},
 {'name': 'Will', 'tvSeries': ''},
 {'name': 'Areo Hotah', 'tvSeries': 'Season 5'}]
```

It now seems like there's a few characters that never appeared in a series. Let's remove these.

## Subset

To make this subset we can use `.keep()`.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")

(clump
  .select('name', 'tvSeries')
  .explode('name', 'tvSeries')
  .keep(lambda d: len(d['tvSeries']) > 0)
  .head(15)
  .collect())
```

This yields:

```python
[{'name': 'Theon Greyjoy', 'tvSeries': 'Season 1'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 2'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 3'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 4'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 5'},
 {'name': 'Theon Greyjoy', 'tvSeries': 'Season 6'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 1'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 2'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 3'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 4'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 5'},
 {'name': 'Tyrion Lannister', 'tvSeries': 'Season 6'},
 {'name': 'Areo Hotah', 'tvSeries': 'Season 5'},
 {'name': 'Areo Hotah', 'tvSeries': 'Season 6'},
 {'name': 'Cressen', 'tvSeries': 'Season 2'}]
```

## Grouping

We now want to create a collection of names per series. That means
we'll first need to use `.group_by()` and then perform an aggregation
with `.agg()`.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")

(clump
  .select('name', 'tvSeries')
  .explode('name', 'tvSeries')
  .keep(lambda d: len(d['tvSeries']) > 0)
  .group_by('tvSeries')
  .agg(names=('name', 'values'))
  .head(2)
  .collect())
```

This yields.

```python
[{'tvSeries': 'Season 3',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Asha Greyjoy',
   'Barristan Selmy',
   'Brandon Stark',
   'Brienne of Tarth',
   'Catelyn Stark',
   'Cersei Lannister',
   'Jaime Lannister',
   'Jon Snow',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 6',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Areo Hotah',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Brandon Stark',
   'Brienne of Tarth',
   'Cersei Lannister',
   'Eddard Stark',
   'Jon Snow',
   'Aeron Greyjoy',
   'Kevan Lannister',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']}]
```

As a final step, we'd now like to sort this per season.

## Sorting

Because there's still a group active we need to remove it before using `.sort()`.

```python
from clumper import Clumper

clump = Clumper.read_json("https://calmcode.io/datasets/got.json")

(clump
  .select('name', 'tvSeries')
  .explode('name', 'tvSeries')
  .keep(lambda d: len(d['tvSeries']) > 0)
  .group_by('tvSeries')
  .agg(names=('name', 'values'))
  .ungroup()
  .sort(lambda d: d['tvSeries'])
  .collect())
```

This yields:

```python
[{'tvSeries': 'Season 1',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Daenerys Targaryen',
   'Arya Stark',
   'Barristan Selmy',
   'Brandon Stark',
   'Catelyn Stark',
   'Cersei Lannister',
   'Eddard Stark',
   'Jaime Lannister',
   'Jon Snow',
   'Kevan Lannister',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 2',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Cressen',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Asha Greyjoy',
   'Brandon Stark',
   'Brienne of Tarth',
   'Catelyn Stark',
   'Cersei Lannister',
   'Jaime Lannister',
   'Jon Snow',
   'Kevan Lannister',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 3',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Asha Greyjoy',
   'Barristan Selmy',
   'Brandon Stark',
   'Brienne of Tarth',
   'Catelyn Stark',
   'Cersei Lannister',
   'Jaime Lannister',
   'Jon Snow',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 4',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Asha Greyjoy',
   'Barristan Selmy',
   'Brandon Stark',
   'Brienne of Tarth',
   'Cersei Lannister',
   'Jaime Lannister',
   'Jon Snow',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 5',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Areo Hotah',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Barristan Selmy',
   'Brienne of Tarth',
   'Cersei Lannister',
   'Jaime Lannister',
   'Jon Snow',
   'Kevan Lannister',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']},
 {'tvSeries': 'Season 6',
  'names': ['Theon Greyjoy',
   'Tyrion Lannister',
   'Areo Hotah',
   'Daenerys Targaryen',
   'Davos Seaworth',
   'Arya Stark',
   'Brandon Stark',
   'Brienne of Tarth',
   'Cersei Lannister',
   'Eddard Stark',
   'Jon Snow',
   'Aeron Greyjoy',
   'Kevan Lannister',
   'Melisandre',
   'Samwell Tarly',
   'Sansa Stark']}]
```
