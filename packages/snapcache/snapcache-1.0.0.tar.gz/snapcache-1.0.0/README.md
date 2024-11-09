# SnapCache

<a href="https://pypi.python.org/pypi/snapcache"><img src="http://img.shields.io/pypi/v/snapcache.svg" alt="Latest version on PyPI"></a> <a href="https://pypi.python.org/pypi/snapcache"><img src="https://img.shields.io/pypi/pyversions/snapcache.svg" alt="Compatible Python versions."></a>

Snap-in memory caching for Python, no persistence, just pure function result caching.

## Motivation

Python’s built-in `functools.lru_cache` offers an easy way to cache function results, but it has limitations. For example, attempting to cache complex objects like `NumPy` arrays results in a `TypeError: unhashable type: 'numpy.ndarray'`.

**SnapCache** addresses this issue by offering a similar simple decorator interface while supporting caching for any data structure ✨.

## Installation

To install **SnapCache**, use `pip`:

```bash
pip install snapcache
```

## Usage

### Function-level Caching

You can cache function results using the `WithCache` decorator. Just apply it to any function you want to memoize.

```python
from snapcache import WithCache

@WithCache(maxsize=3)
def add(a, b):
    return a + b

# Call the function multiple times
print(add(1, 2))  # First call, result is computed and cached
print(add(1, 2))  # Second call, result is retrieved from cache
```

### Method-level Caching

You can also apply the decorator to class methods:

```python
class Foo:
    @WithCache(maxsize=3)
    def bar(self, a, b):
        return a - b

foo = Foo()
print(foo.bar(10, 5))  # First call, result is computed and cached
print(foo.bar(10, 5))  # Second call, result is retrieved from cache
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
