import sys

from typing import Union, Callable

from . import *
from .path import *
from .file import *
from .file import head as _head
from .file import tail as _tail
from .file import skip as _skip
from .file import before as _before
from .file import grep as _grep
from .utils import ls as _ls
from .utils import find as _find
from .utils import cd as _cd
from .utils import mv as _mv
from .utils import cp as _cp
from .utils import rm as _rm
from .utils import mkdir as _mkdir
from .utils import sh as _sh
from .utils import sh_with_stdout as _sh_with_stdout
from .utils import cat as _cat
from .path import cwd as _cwd
from .command import Command


before = Command(_before)
cat = Command(_cat)
cd = Command(_cd, bare_call=True)
cp = Command(_cp)
cwd = Command(_cwd, bare_call=True)
find = Command(_find)
grep = Command(_grep)
head = Command(_head)
ls = Command(_ls, bare_call=True)
mkdir = Command(_mkdir)
mv = Command(_mv)
rm = Command(_rm)
sh = Command(_sh)
sh_with_stdout = Command(_sh_with_stdout)
skip = Command(_skip)
tail = Command(_tail)


def set_ps1(prompt: Union[str, Callable]):
    if callable(prompt):

        class P:
            def __str__(self):
                return prompt()

        sys.ps1 = P()
    else:
        sys.ps1 = prompt
