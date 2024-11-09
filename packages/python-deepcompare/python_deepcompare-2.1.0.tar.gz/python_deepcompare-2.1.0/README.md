deepcompare
===========

[![PyPI](https://badge.fury.io/py/deepcompare.svg)](https://pypi.org/project/deepcompare/)
[![Test Status](https://github.com/anexia/python-deepcompare/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/python-deepcompare/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/anexia/python-deepcompare/branch/main/graph/badge.svg)](https://codecov.io/gh/anexia/python-deepcompare)

`deepcompare` is a library to deeply compare data structures with each other. It can check if two data
structures contain the same data, or if a data structure is a subset of another data structure. The library
supports `Sequence` (e.g. `list` or `tuple`) and `Mapping` (e.g. `dict`) types for the deep comparison.

# Installation

With a [correctly configured](https://pipenv.pypa.io/en/latest/basics/#basic-usage-of-pipenv) `pipenv` toolchain:

```sh
pipenv install python-deepcompare
```

You may also use classic `pip` to install the package:

```sh
pip install python-deepcompare
```

# Getting started

## How it works
 - As a default, the comparison treats all `Sequence` and all `Mapping` types the same (e.g. `(1, 2, 3)` is equal to
   `[1, 2, 3]`). To enable strict type checks, use the `strict` keyword argument.
 - The `partial_compare` method checks if the data structure given as the second parameter is a subset of the data
   structure given as the first parameter.
   - For `Mapping` types this means, that all keys of the second data structure are also keys on the first data
     structure, and the values of the keys are also equal (e.g. `{'a': 1, 'b': 2}` is a subset
     of `{'a': 1, 'b': 2, 'c': 3}`, but `{'a': 1, 'b': 2, 'd': 4}` is not).
   - For `Sequence` types this means, that all values of the second data structure are also values of the first data
     structure, and the values are in the same order (e.g. `[1, 3, 5]` is a subset
     of `[1, 2, 3, 4, 5]`, but `[1, 5, 3]` is not).

## Usage

```python
import deepcompare

# test if two data structures are equal, but the types to not need to match exactly
deepcompare.compare(
    {'key1': (1, 2, 3), 'key2': {'key3': [4, 5, 6]}},
    {'key1': [1, 2, 3], 'key2': {'key3': (4, 5, 6)}},
)  # returns: True

# test if two data structures are equal, and make sure the types match exactly
deepcompare.compare(
    {'key1': (1, 2, 3), 'key2': {'key3': [4, 5, 6]}},
    {'key1': [1, 2, 3], 'key2': {'key3': (4, 5, 6)}},
    strict=True,
)  # returns: False

# test if the second data structure is contained within the first, but
# the types to not need to match exactly
deepcompare.partial_compare(
    {'key1': (1, 2, 3), 'key2': {'key3': [4, 5, 6]}, 'key4': True},
    {'key1': [1, 2], 'key2': {'key3': (4, 6)}},
)  # returns: True

# test if the second data structure is contained within the first, and
# make sure the types match exactly
deepcompare.partial_compare(
    {'key1': (1, 2, 3), 'key2': {'key3': [4, 5, 6]}, 'key4': True},
    {'key1': [1, 2], 'key2': {'key3': (4, 6)}},
    strict=True,
)  # returns: False
```

# List of developers

* Andreas Stocker <AStocker@anexia-it.com>, Lead Developer
