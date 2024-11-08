def require_list(x, len=None):
    import builtins as py

    if isinstance(x, list):
        if len and py.len(x) != len:
            if py.len(x) == 1:
                x *= len
            else:
                raise ValueError(f"expected {len} items, but got {py.len(x)}")
    else:
        return [x] * (len or 1)

def require_grid(x, rows=None, cols=None):
    """
    Require that the given input `x` is a list-of-lists, possibly with a 
    specific number of rows and columns.

    The main role of this function is to allow `x` to be specified more 
    succinctly when the same values are used for each row/column.  Here are the 
    rules for how `x` is interpreted:
    
    - If the input is not a list, it will be made into a list-of-lists.  If the 
      numbers of rows/cols is specified, the output  of the given shape.  
    
    - If the input is a list, it must be a list-of-lists.  If a shape is 
      specified, the input must have that shape.  One special case: if the 
      input has only one row and more are expected, that row will be repeated 
      to get the expected number.
    """
    
    if isinstance(x, list):
        if rows and len(x) != rows:
            if len(x) == 1:
                x *= rows
            else:
                raise ValueError(f"expected {rows} rows, but got {len(x)}")

        for row in x:
            if not isinstance(row, list):
                raise ValueError(f"expected list-of-lists, but got list-of: {type(row)}")
            if cols and len(row) != cols:
                raise ValueError(f"expected {cols} columns, but got {len(row)}")

        return x

    else:
        grid = []

        for i in range(rows or 1):
            row = []
            grid.append(row)

            for j in range(cols or 1):
                row.append(x)

        return grid

def require_array(x, shape):
    raise NotImplementedError


def require_shape(shape, ndim=None, slice_ok=False):
    if slice_ok:
        scalar_types = int, slice
        scalar_types_str = 'int | slice'
    else:
        scalar_types = int
        scalar_types_str = 'int'

    if isinstance(shape, scalar_types):
        shape = (shape,)

    if not isinstance(shape, tuple):
        raise ValueError(f"expected `tuple[{scalar_types_str}]`, got: {shape!r}")

    if not all(isinstance(x, scalar_types) for x in shape):
        raise ValueError(f"expected `tuple[{scalar_types_str}]`, got: {shape!r}")

    if ndim and len(shape) != ndim:
        raise ValueError(f"expected {ndim} dimensions, got: {shape!r}")

    return shape

def require_int(x):
    if not isinstance(x, int):
        raise ValueError(f"expected `int`, got: {x!r}")

    return x


