import os
import re
import builtins
from typing import Union, IO
from collections.abc import Iterable

from .path import Path
from .stream import Stream


class FileStream(Stream):
    def __init__(self, file: IO[str] | Iterable):
        super().__init__(file)
        self._owned_file = None

    def close(self):
        if self._owned_file is not None:
            self._owned_file.close()

        super().close()

    @property
    def closed(self):
        return self._owned_file is not None and self._owned_file.closed

    @classmethod
    def wrap(cls, path_or_file: Union[str, Path, IO[str]]):
        if isinstance(path_or_file, (str, Path)):
            f = builtins.open(path_or_file)
            new = cls(f)
            new._owned_file = f
            return new
        else:
            return cls(path_or_file)


def open(path: str, mode="r") -> FileStream:
    if mode != "r":
        raise ValueError("Only r mode is supported for text streams.")

    return FileStream(builtins.open(path))


def human(size, use_si=False):
    "Convert number of bytes into human readable size."
    s = size
    u = ""
    d = 10**3 if use_si else 2**10
    for unit in ("K", "M", "G", "T", "E", "P"):
        if s < d:
            break
        s /= d
        u = unit

    return s, u


def size(path):
    "Return the size of path in bytes."
    return os.stat(path).st_size


# FIXME Right now all the following functions are eager
# because the wrapper needs to read the file before it is closed.
# I need to figure a proper way of providing a lazy stream of lines.
# For that, the wrapper should pass the closing procedure down the pipe.


def head(path_or_file: Union[str, IO[str]], n=10):
    "Iterate over the n first lines of path."
    with FileStream.wrap(path_or_file) as f:
        return Stream(f.islice(n))


def tail(path_or_file: Union[str, IO[str]], n=10):
    "Iterate over the n last lines of path."
    with FileStream.wrap(path_or_file) as f:
        return Stream(f.tail(n))


def skip(path_or_file: Union[str, IO[str]], n=10):
    "Iterate over the lines of path after the nth."
    with FileStream.wrap(path_or_file) as f:
        for _ in zip(range(n), f):
            pass
        return Stream(list(f))


def before(path_or_file: Union[str, IO[str]], n=10):
    "Iterate over the lines of path but stop before the last n."
    with FileStream.wrap(path_or_file) as f:
        return Stream(list(f.before(n)))


def last(path_or_file: Union[str, IO[str]]):
    with FileStream.wrap(path_or_file) as f:
        for last in f:
            pass
        return Stream(list(last))


def grep(path_or_file: Union[str, IO[str]], pattern):
    "Iterate over the lines from path that match pattern."
    r = re.compile(pattern)
    f = FileStream.wrap(path_or_file)

    def matcher(e):
        return r.match(e) is not None

    return f.filter(matcher)
