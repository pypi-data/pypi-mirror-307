from .interpreter import Interpreter
from . import interactive

def main():
    interp.interact()

interp = Interpreter(local=interactive.__dict__)


if __name__ == "__main__":
    main()
