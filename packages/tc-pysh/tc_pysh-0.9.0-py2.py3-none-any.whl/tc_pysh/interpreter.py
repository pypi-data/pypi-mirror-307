from code import InteractiveConsole
import readline
import rlcompleter


class Interpreter(InteractiveConsole):
    """A Python REPL.

    This aims at reproducing the behavior of Python REPL, including the
    autocompletion feature offered by readline.
    """

    def __init__(self, local=None):
        self.local = local if local is not None else {}
        super().__init__(local)
        readline.set_completer(rlcompleter.Completer(self.local).complete)
        readline.parse_and_bind("tab: complete")
