<img src="logo.png" width=185 height=185 align="right">

# **Clumper**

**A small library that can clump sequences of data together.**

Part of a video series on [calmcode.io](https://calmcode.io).

## Features

- This library only has optional dependencies. Just a modern version of python gives you 99% of the features.
- The library offers a pattern of verbs that are very expressive.
- You can write code from top to bottom, left to right.
- You can read in many `json`/`yaml`/`csv` files at once by using a wildcard `*`.
- You can directly read data from a web-endpoint.
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

Make sure you check out the [issue list](https://github.com/koaning/clumper/issues)
beforehand. New features should be discussed first and we also want to prevent
that two people are working on the same thing. To get started locally, you can clone
the repo and quickly get started using the `Makefile`.

```
git clone git@github.com:koaning/clumper.git
cd clumper
make install-dev
```

### Bugs

If you encounter a bug, we'd love to hear about it!
We would appreciate though if you could add a reproducible
example when you [submit an issue on github](https://github.com/koaning/clumper/issues/new/choose).

We've included some methods to our library to make this
relatively easy. Here's an example of a reproducible code-block.

```python
from clumper import Clumper

data = [{"a": 1}, {"a": 2}]

clump = Clumper(data)
expected = [{"a": 1}, {"a": 2}]
assert clump.equals(expected)
```

Note how this block uses `.equals()` to demonstrate
what the expected output is. This is great for maintainers
because they can just copy the code and work on a fix.

## Origin Stories

### Why the name?

Sometimes you just want something to "clump" together in the right way.
So we turned the word "clump" into a verb and into a python package.

### How did it get started?

The origin of this package was educational. It got
started as free educational content on [calmcode.io](https://calmcode.io)
to demonstrate how to make your own package. If you're interested in learning
how this package got made you can watch a small documented series of the
lessons learned.
