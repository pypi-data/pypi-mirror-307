from typing import Callable, Any

def make_array(shape: tuple[int], init: Callable[[tuple[int]], Any]):
    """
    Create an array of nested lists.

    Arguments:
        shape:
            The size of array to create.  Each entry in this tuple specifies 
            the size of the corresponding dimension.

        init:
            A function that will be used to get an initial value for each item 
            in the array.  The function will be called with an index as its 
            only argument.  The index will always a tuple of integers (even for 
            a 1D array) with one entry for each dimension of the array.  The 
            function can return any value.
    """
    if len(shape) == 0:
        return init(())

    if len(shape) == 1:
        return [init((i,)) for i in range(shape[0])]

    return [
        make_array(
            shape[1:],
            init=lambda idx, i=i: init((i, *idx))
        )
        for i in range(shape[0])
    ]

def get(array: list, ijk):
    if isinstance(ijk, int):
        return array[ijk]

    for i in ijk:
        array = array[i]

    return array

def ndim(array):
    raise NotImplementedError

def shape(array):
    raise NotImplementedError

