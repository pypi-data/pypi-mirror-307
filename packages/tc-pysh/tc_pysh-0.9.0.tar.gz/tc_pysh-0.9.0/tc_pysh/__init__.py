from .path import AbsolutePath, ensure_path, ensure_abs_path, Path, RelativePath, cwd
from .query import Query
from .utils import (
    archive,
    cat,
    cd,
    cp,
    find,
    in_dir,
    ls,
    mkdir,
    mv,
    rm,
    sh,
    sh_with_stdout,
)
from .file import open


__version__ = "0.9.0"


# I use that for the automatic doc
__all__ = [
    "AbsolutePath",
    "archive",
    "cat",
    "cd",
    "cp",
    "cwd",
    "ensure_abs_path",
    "ensure_path",
    "find",
    "in_dir",
    "ls",
    "mkdir",
    "mv",
    "Path",
    "open",
    "Query",
    "RelativePath",
    "rm",
    "sh",
    "sh_with_stdout",
]
