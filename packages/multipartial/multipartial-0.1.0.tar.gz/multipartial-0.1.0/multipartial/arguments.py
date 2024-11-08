from reprfunc import repr_from_init

class Multiargument:
    __repr__ = repr_from_init()

    def require_ndim(self):
        raise NotImplementedError

    def require_dim_size(self, ijk):
        raise NotImplementedError

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
        min_ijk = []
        max_ijk = []

        for i in region:
            match i:
                case int():
                    min_ijk.append(i)
                    max_ijk.append(i)
                case slice():
                    min_ijk.append(i.start)
                    max_ijk.append(j if (j := i.stop) is None else j - 1)
                case _:
                    raise AssertionError

        self.min_ijk = tuple(min_ijk)
        self.max_ijk = tuple(max_ijk)
        self.inside = inside
        self.outside = outside

    def require_ndim(self):
        return len(self.min_ijk)

    def require_dim_size(self, i):
        return 0

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

