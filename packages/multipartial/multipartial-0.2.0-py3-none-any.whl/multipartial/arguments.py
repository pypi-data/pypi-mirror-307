from reprfunc import repr_from_init

class Multiargument:
    __repr__ = repr_from_init()

    def require_ndim(self):
        raise NotImplementedError

    def require_dim_size(self, ijk):
        raise NotImplementedError

    def on_resolve_shape(self, shape):
        pass

    def get_value(self, ijk):
        raise NotImplementedError

class Dimension(Multiargument):

    def __init__(self, dim, values, scalar_types=(str, bytes)):
        self.dim = dim
        self.values = values
        self.broadcast = is_scalar(values, scalar_types)

    @classmethod
    def from_varargs(cls, dim, *values):
        return cls(dim, values)

    def require_ndim(self):
        return self.dim + 1

    def require_dim_size(self, i):
        if i != self.dim or self.broadcast:
            return 0
        else:
            return len(self.values)

    def get_value(self, ijk):
        if self.broadcast:
            return self.values
        else:
            return self.values[ijk[self.dim]]

class Put(Multiargument):

    def __init__(self, region, inside, outside):
        self.region = region
        self.inside = inside
        self.outside = outside

    def require_ndim(self):
        return len(self.region)

    def require_dim_size(self, i):
        return 0

    def on_resolve_shape(self, shape):
        min_ijk = []
        max_ijk = []

        def index_from_int(x, i):
            x_orig = x
            if x < 0:
                x += shape[i]
            if x < 0 or x >= shape[i]:
                raise IndexError(f"index {x_orig} is out of bounds for dimension {i} (size {shape[i]})")
            return x

        def index_from_slice_start(x, i):
            return index_from_int(x.start or 0, i)

        def index_from_slice_stop(x, i):
            y = (shape[i] if x.stop is None else x.stop) - 1
            return index_from_int(y, i)

        for i, x in enumerate(self.region):
            match x:
                case int():
                    min_ijk.append(index_from_int(x, i))
                    max_ijk.append(index_from_int(x, i))
                case slice():
                    min_ijk.append(index_from_slice_start(x, i))
                    max_ijk.append(index_from_slice_stop(x, i))
                case _:
                    raise AssertionError

        self.min_ijk = tuple(min_ijk)
        self.max_ijk = tuple(max_ijk)

    def get_value(self, ijk):
        above_min = all(
            i >= i_min if i_min is not None else True
            for i, i_min in zip(ijk, self.min_ijk, strict=True)
        )
        below_max = all(
            i <= i_max if i_max is not None else True
            for i, i_max in zip(ijk, self.max_ijk, strict=True)
        )
        return self.inside if above_min and below_max else self.outside

class Const(Multiargument):

    def __init__(self, value):
        self.value = value

    def require_ndim(self):
        return 0

    def require_dim_size(self, i):
        return 0

    def get_value(self, ijk):
        return self.value

def is_scalar(x, scalar_types=(str, bytes)):
    if scalar_types and isinstance(x, scalar_types):
        return True

    try:
        iter(x)
    except TypeError:
        return True

    return False

