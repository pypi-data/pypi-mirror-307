import os
import os.path
import shutil
import shlex
import subprocess
import sys
from io import BytesIO

from contextlib import contextmanager

from typing import Optional, Iterator, Union, List

from .path import AbsolutePath, ensure_abs_path, Path, SPath, RelativePath, cwd
from .zipper import Zipper
from .query import Query


def makeparam(default):
    "Create a parameter/cell/box object."

    def func(set=None):
        if set is None:
            return func.state
        else:
            func.state = set

    func.state = default
    return func


debug = makeparam(False)


def find(path: Optional[SPath] = None, relative=False) -> Query:
    """Create a `Query` to recursively look for path under `path`.

    :param path: (optional, `cwd()`) a `str` or a `Path` target
    :param relative: (optional, False) wether to yield `RelativePath` or `AbsolutePath`
    """

    def walker() -> Iterator[Union[AbsolutePath, RelativePath]]:
        _path: AbsolutePath
        if path is None:
            _path = cwd()
        else:
            _path = ensure_abs_path(path)

        pwd = cwd()

        for dir, _, files in os.walk(str(_path)):
            if dir.startswith("/"):
                d = AbsolutePath.from_str(dir)
            else:
                d = RelativePath.from_str(dir).at(_path)

            if relative:
                d = d.relative_to(pwd)

            yield d
            yield from (d.add(file) for file in files)

    return Query(walker())


def ls(path: Optional[SPath] = None, relative: bool = False) -> Query:
    """Create a `Query` on the direct content of `path`

    :param path: (optional, `cwd()`) a `str` or a `Path` target
    :param relative: (optional, True) wether to yield `RelativePath` or `AbsolutePath`
    """

    def walker() -> Iterator[Union[AbsolutePath, RelativePath]]:
        if path is None:
            _path = cwd()
        else:
            _path = ensure_abs_path(path)

        if relative:
            yield from map(RelativePath, os.listdir(_path))
        else:
            for name in os.listdir(_path):
                yield _path.add(name)

    return Query(walker())


def mv(*args: SPath, force=False):
    """Move a set of source to a single target (like shell `mv`).

    :param *args: Path or str, the last one is the target
    """
    if len(args) == 1:
        raise ValueError("mv needs at least two parameters.")
    else:
        dest, *srcs = reversed(list(map(ensure_abs_path, args)))
        if dest.isdir():
            for src in srcs:
                b = src.base
                fdest = dest.add(b)
                if not force and fdest.exists():
                    raise ValueError(f"File {fdest} already exists.")

            for src in srcs:
                b = src.base
                fdest = dest.add(b)
                if debug():
                    print(f"mv {src} {fdest}")
                else:
                    os.replace(src, fdest)
        else:
            if len(srcs) > 1:
                raise ValueError(
                    "mv cannot move more than one source" " to the same dest"
                )
            if not force and dest.exists():
                raise ValueError(f"File {dest} already exists.")
            src = srcs[0]
            if debug():
                print(f"mv {src} {dest}")
            else:
                os.replace(src, dest)


def cp(*args: SPath, force=False):
    """Copy a set of source to a target (like shell `cp`).

    :param *args: Path or str, the last one is the target
    """
    if len(args) <= 1:
        raise ValueError("cp needs at least two parameters.")
    else:
        dest, *srcs = reversed(list(map(ensure_abs_path, args)))
        if dest.isdir():
            for src in srcs:
                b = src.base
                fdest = dest.add(b)
                if not force and fdest.exists():
                    raise ValueError(f"File {fdest} already exists.")

            for src in srcs:
                b = src.base
                fdest = dest.add(b)
                if debug():
                    print(f"cp -r {src} {fdest}")
                elif src.isdir():
                    shutil.copytree(src, fdest)
                else:
                    shutil.copy(src, fdest)
        else:
            if len(srcs) > 1:
                raise ValueError("cp cannot move more than one source to the same dest")
            if not force and dest.exists():
                raise ValueError("File already exists.")
            src = srcs[0]
            if debug():
                print(f"cp -r {src} {dest}")
            elif src.isdir():
                shutil.copytree(src, dest)
            else:
                shutil.copy(src, dest)


def rm(*args: SPath, recursive=False, force=False):
    """Remove files and directories.

    :param *args: Path objects to remove.
    :param recursive: Recursively remove into directories.
    :param force: Force remove: does not raise an exception on failure.
    """
    if recursive:
        for p in map(ensure_abs_path, args):
            if p.isfile():
                os.remove(p)
            else:
                shutil.rmtree(p, ignore_errors=force)
    else:
        if force:
            for p in map(ensure_abs_path, args):
                try:
                    if debug():
                        print(f"rm -rf {p}")
                    else:
                        os.remove(p)
                except Exception:
                    pass
        else:
            for p in map(ensure_abs_path, args):
                if debug():
                    print(f"rm -f {p}")
                else:
                    os.remove(p)


def mkdir(path: SPath, exist_ok=True):
    """Create a leaf directory and all intermedite ones.

    :param path: Target directory
    :param exist_ok: if False and path already exists, raise a `FileExistsError`
    """
    if debug():
        print(f"mkdir -p {path}")
    else:
        os.makedirs(ensure_abs_path(path), exist_ok=exist_ok)


def archive(dest: SPath, *args: SPath, transform=None, format="tar.gz"):
    """Create a new archive containing a set of files."""
    if debug():
        raise NotImplementedError("archive is not yet supported in debug mode.")

    z = Zipper(format)
    if args:
        with z.open(ensure_abs_path(dest)) as ar:
            for f in map(ensure_abs_path, args):
                ar.add(f, transform=transform)
    else:
        return z.open(ensure_abs_path(dest))


def cd(to: Optional[SPath] = None):
    """Change current working directory."""
    if to is None:
        to = AbsolutePath.from_str("~")
    path = ensure_abs_path(to)
    os.chdir(path)


@contextmanager
def in_dir(d: Optional[SPath] = None):
    """Context manager to temporarily change current working directory."""
    current = cwd()
    cd(d)
    try:
        yield
    finally:
        cd(current)


def sh(command: Union[str, List[Union[str, Path]]], path: Optional[SPath] = None):
    """Run a shell command.

    :param command: command to run as a string or as a list of parameters.
    :param path: (optiona) working directory to run the command.
    :returns: command return code
    """
    if isinstance(command, str):
        cmd = command
    else:
        cmd = " ".join(shlex.quote(str(c)) for c in command)

    cwd = ensure_abs_path(path).to_str() if path else None

    return subprocess.call(cmd, shell=True, cwd=cwd)


def sh_with_stdout(
    command: Union[str, List[Union[str, Path]]], path: Optional[SPath] = None
):
    """Run a shell command.

    :param command: command to run as a string or as a list of parameters.
    :param path: (optiona) working directory to run the command.
    :returns: the content of stdout.
    """
    if isinstance(command, str):
        cmd = command
    else:
        cmd = " ".join(shlex.quote(str(c)) for c in command)

    cwd = ensure_abs_path(path).to_str() if path else None

    return subprocess.run(
        cmd, shell=True, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE
    ).stdout


def cat(*sources, dest=None, append=False):
    """Similar to cat command.

    `cat(a, b, c, ..., dest=dest)` copy the content of a, b, c, ... into dest.

    :param *sources: the source files. If none are provided, read from stdin.
    """
    if len(sources) == 0:
        sources = [sys.stdin]

    if dest is None:
        destf = sys.stdout.buffer
    elif append:
        destf = open(dest, "ab")
    else:
        destf = open(dest, "wb")

    try:
        # TODO use sendfile on posix for faster write
        for src in sources:
            with open(src, "rb") as srcf:
                for line in srcf:
                    destf.write(line)
    finally:
        if destf is not sys.stdout.buffer:
            destf.close()
