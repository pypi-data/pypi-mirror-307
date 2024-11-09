Multipartial
============

[![Last release](https://img.shields.io/pypi/v/multipartial.svg)](https://pypi.python.org/pypi/multipartial)
[![Python version](https://img.shields.io/pypi/pyversions/multipartial.svg)](https://pypi.python.org/pypi/multipartial)
[![Documentation](https://img.shields.io/readthedocs/multipartial.svg)](https://multipartial.readthedocs.io/en/latest/)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/multipartial/test.yml?branch=master)](https://github.com/kalekundert/multipartial/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/multipartial)](https://app.codecov.io/github/kalekundert/multipartial)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/multipartial?logo=github)](https://github.com/kalekundert/multipartial)

*Multipartial* is a library for constructing N-dimensional arrays of partial 
functions.  For example, the following snippet shows how to make a 2x3 grid of 
partial functions where the `a` argument varies by row, the `b` argument varies 
by column, the `c` argument is always the same, and the `d` argument is 
specified at call-time:

```
>>> from multipartial import multipartial, dim
>>> def f(a, b, c, d):
...     return a, b, c, d
...
>>> grid = multipartial(f, a=dim[0](1, 2), b=dim[1](3, 4, 5), c=6)
>>> grid[0][0](d=7)
(1, 3, 6, 7)
>>> grid[0][1](d=8)
(1, 4, 6, 8)
>>> grid[0][2](d=9)
(1, 5, 6, 9)
>>> grid[1][0](d=10)
(2, 3, 6, 10)
>>> grid[1][1](d=11)
(2, 4, 6, 11)
>>> grid[1][2](d=12)
(2, 5, 6, 12)
```

