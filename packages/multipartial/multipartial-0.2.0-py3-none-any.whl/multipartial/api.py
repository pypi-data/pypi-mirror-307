from .brackets import BracketFactory, ALL
from .partial import Multipartial
from .arguments import Dimension, Put
from .require import require_shape, require_int
from functools import partial

multipartial = BracketFactory(
        name='multipartial',
        custom_init=lambda x: Multipartial(require_shape(x, slice_ok=True)),
        default_init=lambda: Multipartial(None),
)
partial_list = BracketFactory(
        name='partial_list',
        custom_init=lambda x: Multipartial(require_shape(x, ndim=1, slice_ok=True)),
        default_init=lambda: Multipartial((ALL,)),
)
partial_grid = BracketFactory(
        name='partial_grid',
        custom_init=lambda x: Multipartial(require_shape(x, ndim=2, slice_ok=True)),
        default_init=lambda: Multipartial((ALL, ALL)),
)

dim = BracketFactory(
        name='dim',
        custom_init=lambda x: partial(Dimension.from_varargs, require_int(x)),
        default_init=lambda: partial(Dimension.from_varargs, 0),
)
Dim = BracketFactory(
        name='Dim',
        custom_init=lambda x: partial(Dimension, require_int(x)),
        default_init=lambda: partial(Dimension, 0),
)
rows = partial(Dimension.from_varargs, 0)
cols = partial(Dimension.from_varargs, 1)

put = BracketFactory(
        name='put',
        custom_init=lambda x: partial(Put, require_shape(x, slice_ok=True)),
)
