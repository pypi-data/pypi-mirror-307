ALL = slice(None)

class BracketFactory:

    def __init__(self, name, custom_init, default_init=None):
        self.__name__ = name
        self.custom_init = custom_init
        self.default_init = default_init

    def __repr__(self):
        return self.__name__

    def __getitem__(self, args):
        return self.custom_init(args)

    def __call__(self, *args, **kwargs):
        if not self.default_init:
            raise TypeError(f"`{self.__name__}` object is not callable, did you mean `{__name__}[...]`?")

        f = self.default_init()
        return f(*args, **kwargs)

