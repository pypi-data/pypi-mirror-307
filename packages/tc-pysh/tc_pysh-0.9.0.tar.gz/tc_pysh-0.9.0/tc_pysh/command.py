from .path import Path
from .stream import Stream


class Command:
    def __init__(self, obj, bare_call=False):
        self.obj = obj
        self.bare_call = bare_call

    def __call__(self, *args, **kwargs):
        r = self.obj(*args, **kwargs)

        if isinstance(r, Path) or isinstance(r, Stream):
            return Command(r)

        return r

    def __getattr__(self, name):
        if name == "obj":
            return super().__getattribute__("obj")
        return Command(getattr(self.obj, name))

    def __repr__(self):
        if self.bare_call and callable(self.obj):
            r = self.obj()
        else:
            r = self.obj

        if isinstance(r, (str, bytes)):
            txt = repr(r)
        elif isinstance(r, Path):
            txt = str(r)
        elif isinstance(r, Stream):
            txt = "\n".join(map(str, r))
        else:
            txt = str(r)
        return txt
