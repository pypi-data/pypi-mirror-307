"""
N-dimensional arrays of partial functions.
"""

__version__ = '0.2.0'

from .api import (
        multipartial, partial_list, partial_grid,
        dim, Dim, rows, cols, put,
)
from .require import require_list, require_grid, require_array
