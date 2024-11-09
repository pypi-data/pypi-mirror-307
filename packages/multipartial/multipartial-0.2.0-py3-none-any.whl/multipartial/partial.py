from .arguments import Multiargument, Const
from .brackets import ALL
from .array import make_array
from functools import partial

class Multipartial:

    def __init__(self, shape):
        self.shape = shape

    def __call__(self, func, *args, **kwargs):
        wrapped_args = [
                x if isinstance(x, Multiargument) else Const(x)
                for x in args
        ]
        wrapped_kwargs = {
                k: v if isinstance(v, Multiargument) else Const(v)
                for k, v in kwargs.items()
        }

        multiargs = wrapped_args + list(wrapped_kwargs.values())
        shape = resolve_shape(self.shape, multiargs)

        for arg in multiargs:
            arg.on_resolve_shape(shape)

        def make_func_i(i):
            args_i = [x.get_value(i) for x in wrapped_args]
            kwargs_i = {k: v.get_value(i) for k, v in wrapped_kwargs.items()}
            return partial(func, *args_i, **kwargs_i)

        return make_array(shape, init=make_func_i)

def resolve_shape(shape, multiargs):
    shape = resolve_ndim(shape, multiargs)
    return tuple(
            resolve_dim_size(i, shape[i], multiargs)
            for i in range(len(shape))
    )

def resolve_ndim(shape, multiargs):
    if shape is not None:
        n = len(shape)
        for arg in multiargs:
            m = arg.require_ndim() 
            if m > n:
                raise ValueError(f"array has {n} dimension(s), but argument has {m}")

        return shape

    else:
        n = max(
                arg.require_ndim()
                for arg in multiargs
        )
        return n * [ALL]

def resolve_dim_size(i, size, multiargs):
    if size == slice(None):
        sizes = {
                x.require_dim_size(i)
                for x in multiargs
        }
        sizes.discard(0)

        if len(sizes) == 0:
            return 1

        if len(sizes) > 1:
            raise ValueError(f"found different-length arguments for dimension {i}: {sizes}")

        return sizes.pop()

    else:
        for arg in multiargs:
            n = arg.require_dim_size(i)
            if n and n != size:
                raise ValueError(f"expected {size} argument(s) for dimension {i}, got {n}")

    return size
