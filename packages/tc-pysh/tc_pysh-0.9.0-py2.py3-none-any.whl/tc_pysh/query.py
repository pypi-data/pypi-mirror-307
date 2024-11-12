import re

from typing import Union, Iterable, Callable

from .stream import Stream
from .path import AbsolutePath, Path, ensure_path, ensure_abs_path


PathPred = Callable[[AbsolutePath], bool]


class Query(Stream):
    "Filter a collection of path"

    def __init__(self, source: Iterable[Path]):
        super().__init__(Stream(source).map(ensure_path))

    def abs(self):
        return self.map(ensure_abs_path)

    def relative(self):
        return self.map(lambda d: d.relative_to("."))

    def isfile(self):
        """Filter paths to keep only the files."""
        return self.filter(lambda p: p.isfile())

    def isdir(self):
        """Filter the elements of the query to keep only the directories."""
        return self.filter(lambda p: p.isdir())

    def name(self, pattern: Union[str, re.Pattern]):
        """Filter the elements of the query to keep only the ones matching `pattern`.

        :param pattern: a `str` or a `re.Pattern`, used as a regex to match the paths
        """
        if isinstance(pattern, re.Pattern):
            regex: re.Pattern = pattern
        else:
            regex = re.compile(pattern)

        def match(path: AbsolutePath):
            return bool(regex.fullmatch(path.base))

        return self.filter(match)

    def endswith(self, suffix: str):
        """Filter the elements of the query based on a suffix.

        :param suffix: the suffix to match
        """
        return self.filter(lambda p: p.base.endswith(suffix))
