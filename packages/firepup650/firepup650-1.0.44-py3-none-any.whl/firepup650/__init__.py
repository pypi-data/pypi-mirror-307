"""Firepup650's PYPI Package"""

fkey, termios, tty = None, None, None
from warnings import warn as ww

try:
    import termios, tty, fkeycapture as fkey
except ImportError:
    ww(
        "Warning! This module has reduced functionality on Windows! I hope you know what you're doing!",
        stacklevel=2,
    )

import os, sys, time, sqlite3, ast, pydoc  # type: ignore[import]
import random as r
import fpsql as fql
from typing import NoReturn, TypeVar, Type, Optional, List, Any, Union
from collections.abc import Iterable


def alias(func):
    """# Function: alias
    !Wrapper
    Overwrites the docstring for a function to the specified function
    # Inputs:
    func

    # Returns:
    None

    # Raises:
    None"""

    def decorator(f):
        f.__doc__ = (
            "This method is an alias of the following method:\n\n"
            + pydoc.text.document(func)
        )
        return f

    return decorator


__VERSION__ = "1.0.42"
__NEW__ = "Small typo fix"
__LICENSE__ = "MIT"


class NotImplementedOnWindowsException(NotImplementedError):
    """Exception raised when a Linux only method is called on a Windows machine"""


def flushPrint(*args) -> None:
    """# Function: flushPrint
      Prints and flushes the provided args.
    # Inputs:
      *args - The args to print

    # Returns:
      None

    # Raises:
      None"""
    print(*args, end="", flush=True)


flush_print = flushPrint


def clear(ascii: bool = True) -> None:
    """# Function: clear
      Clears the screen
    # Inputs:
      ascii: bool - Controls whether or not we clear with ascii, defaults to True

    # Returns:
      None

    # Raises:
      None"""
    if not ascii:
        os.system("clear||cls")
    else:
        flushPrint("\033[H\033[2J")


@alias(os.system)
def cmd(command: str) -> int:
    """# Function: cmd
      Runs bash commands
    # Inputs:
      command: str - The command to run

    # Returns:
      int - Status code returned by the command

    # Raises:
      None"""
    status = os.system(command)
    return status


def randint(low: int = 0, high: int = 10) -> int:
    """# Funcion: randint
      A safe randint function
    # Inputs:
      low: int - The bottom number, defaults to 0
      high: int - The top number, defaults to 10

    # Returns:
      int - A number between high and low

    # Raises:
      None"""
    return r.randint(min(low, high), max(low, high))


@alias(sys.exit)
def e(code: Union[str, int, None] = None) -> NoReturn:
    """# Function: e
      Exits with the provided code
    # Inputs:
      code: Union[str, int, None] - The status code to exit with, defaults to None

    # Returns:
      None

    # Raises:
      None"""
    sys.exit(code)


def gp(
    keycount: int = 1,
    chars: list = ["1", "2"],
    bytes: bool = False,
    allowDelete: bool = False,
    filler: str = "-",
) -> Union[str, bytes]:
    raise NotImplementedOnWindowsException(
        "This method is not implemented for Windows machines"
    )


if fkey:

    def gp(
        keycount: int = 1,
        chars: list = ["1", "2"],
        bytes: bool = False,
        allowDelete: bool = False,
        filler: str = "-",
    ) -> Union[str, bytes]:
        """# Function: gp
          Get keys and print them.
        # Inputs:
          keycount: int - Number of keys to get, defaults to 1
          chars: list - List of keys to accept, defaults to ["1", "2"]
          bytes: bool - Wether to return the kyes as bytes, defaults to False
          allowDelete: bool - Wether to allow deleting chars, defaults to False
          filler: str - The character to use as filler when waiting on more chars, defaults to "-"

        # Returns:
          Union[str, bytes] - Keys pressed

        # Raises:
          None"""
        got = 0
        keys = []
        if allowDelete:
            chars.append(fkey.KEYS["BACKSPACE"].decode())
        flushPrint(filler * keycount)
        while len(keys) < keycount:
            key = fkey.getchars(1, chars, True)  # type: bytes #type: ignore
            if not allowDelete or key != fkey.KEYS["BACKSPACE"]:
                keys.append(key.decode())
            elif len(keys):
                keys.pop()
            flushPrint(f"\033[{keycount}D{''.join(keys)}{filler*(keycount-len(keys))}")
            got += 1
        print()
        if not bytes:
            return "".join(keys)
        else:
            return ("".join(keys)).encode()


def gh(
    keycount: int = 1,
    chars: list = ["1", "2"],
    char: str = "*",
    bytes: bool = False,
    allowDelete: bool = False,
    filler: str = "-",
) -> Union[str, bytes]:
    raise NotImplementedOnWindowsException(
        "This method is not implemented for Windows machines"
    )


if fkey:

    def gh(
        keycount: int = 1,
        chars: list = ["1", "2"],
        char: str = "*",
        bytes: bool = False,
        allowDelete: bool = False,
        filler: str = "-",
    ) -> Union[str, bytes]:
        """# Function: gh
          Get keys and print `char` in their place.
        # Inputs:
          keycount: int - Number of keys to get, defaults to 1
          chars: list - List of keys to accept, defaults to ["1", "2"]
          char: str - Character to use to obfuscate the keys, defaults to *
          bytes: bool - Wether to return the kyes as bytes, defaults to False
          allowDelete: bool - Wether to allow deleting chars, defaults to False
          filler: str - The character to use as filler when waiting on more chars, defaults to "-"

        # Returns:
          Union[str, bytes] - Keys pressed

        # Raises:
          None"""
        got = 0
        keys = []
        if allowDelete:
            chars.append(fkey.KEYS["BACKSPACE"].decode())
        flushPrint(filler * keycount)
        while len(keys) < keycount:
            key = fkey.getchars(1, chars, True)  # type: bytes #type: ignore
            if not allowDelete or key != fkey.KEYS["BACKSPACE"]:
                keys.append(key.decode())
            elif len(keys):
                keys.pop()
            flushPrint(f"\033[{keycount}D{char*len(keys)}{filler*(keycount-len(keys))}")
            got += 1
        print()
        if not bytes:
            return "".join(keys)
        else:
            return ("".join(keys)).encode()


def printt(text: str, delay: float = 0.1, newline: bool = True) -> None:
    raise NotImplementedOnWindowsException(
        "This method is not implemented for Windows machines"
    )


if fkey:

    def printt(text: str, delay: float = 0.1, newline: bool = True) -> None:
        """# Function: printt
          Print out animated text!
        # Inputs:
          text: str - Text to print (could technicaly be a list)
          delay: float - How long to delay between characters, defaults to 0.1
          newline: bool - Wether or not to add a newline at the end of the text, defaults to True

        # Returns:
          None

        # Raises:
          None"""
        # Store the current terminal settings
        original_terminal_settings = termios.tcgetattr(sys.stdin)
        # Change terminal settings to prevent any interruptions
        tty.setcbreak(sys.stdin)
        for char in text:
            flushPrint(char)
            time.sleep(delay)
        if newline:
            print()
        # Restore the original terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_terminal_settings)


@alias(time.sleep)
def sleep(seconds: float = 0.5) -> None:
    """# Function: sleep
      Calls `time.sleep(seconds)`
    # Inputs:
      seconds: float - How long to sleep for, defaults to 0.5

    # Returns:
      None

    # Raises:
      None"""
    time.sleep(seconds)


@alias(r.seed)
def rseed(seed: Any = None, version: int = 2) -> None:
    """# Function: rseed
      reseed the random number generator
    # Inputs:
      seed: Any - The seed, defaults to None
      version: int - Version of the seed (1 or 2), defaults to 2

    # Returns:
      None

    # Raises:
      None"""
    r.seed(seed, version)


setattr(Iterable, "__class_getitem__", lambda x: None)
T = TypeVar("T")


def robj(iterable: Iterable[T]) -> T:
    """# Function: robj
      Returns a random object from the provided iterable
    # Input:
      iterable: Iterable[T] - Any valid Iterable

    # Returns:
      T - A random object of type `T` from the provided iterable

    # Raises:
      None"""
    return r.choice(iterable)  # type: ignore[arg-type]


def Color(
    r: int = 0, g: int = 0, b: int = 0, bcolor: bool = False, flush: bool = True
) -> Union[None, str]:
    """# Function: Color
      Set the text to a specific color.
    # Inputs:
      r: int - The red value, range of 0-255, defaults to 0
      g: int - The green value, range of 0-255, defaults to 0
      b: int - The blue value, range of 0-255, defaults to 0
      bcolor: bool - Wether to return the color as a str, defaults to False
      fulsh: bool - Wether to flushPrint the color, defaults to True

    # Returns:
      Union[None, str] - The color code if `bcolor` is True. Otherwise, returns nothing

    # Raises:
      None"""
    if r < 0:
        r = 0
    if r > 255:
        r = 255
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    if b < 0:
        b = 0
    if b > 255:
        b = 255
    if bcolor:
        return f"\033[38;2;{r};{g};{b}m"
    elif flush:
        flushPrint("\003[0m")
        flushPrint(f"\033[38;2;{r};{g};{b}m")
    else:
        print("\003[0m")
        print(f"\033[38;2;{r};{g};{b}m")
    return None


class bcolors:
    """
    This class contains various pre-defined color codes.
    """

    INVERSE = "\033[8m"

    @staticmethod
    def fINVERSE() -> None:
        """INVERTs foreground and background colors"""
        print("\033[8m", end="")

    RESET = "\033[0m"
    RWHITE: str = f"\033[0m{Color(255,255,255,bcolor=True)}"
    WHITE: str = f"{Color(255,255,255,bcolor=True)}"
    FAILINVERSE: str = f"{Color(255,bcolor=True)}\033[49m\033[7m"

    @staticmethod
    def fWHITE() -> None:
        """Sets the text color to WHITE"""
        print(f"{Color(255,255,255,bcolor=True)}", end="")

    @staticmethod
    def fRWHITE() -> None:
        """RESETs the text color, then sets it to WHITE"""
        print(f"\033[0m{Color(255,255,255,bcolor=True)}", end="")

    @staticmethod
    def fFAILINVERSE() -> None:
        """Sets the text color RED, then inverses it."""
        print(f"{Color(255,bcolor=True)}\033[49m\033[7m", end="")

    @staticmethod
    def fRESET() -> None:
        """RESETs the formatting"""
        print("\033[0m", end="")

    BROWN: str = f"{Color(205,127,50,bcolor=True)}"

    @staticmethod
    def fBROWN() -> None:
        """Sets the text color to BROWN"""
        print(f"{Color(205,127,50,bcolor=True)}", end="")

    WARNING: str = f"{Color(236,232,26,bcolor=True)}"

    @staticmethod
    def fWARNING() -> None:
        """Sets the text color to YELLOW"""
        print(f"{Color(236,232,26,bcolor=True)}", end="")

    FAIL: str = f"{Color(255,bcolor=True)}"

    @staticmethod
    def fFAIL() -> None:
        """Sets the text color to RED"""
        print(f"{Color(255,bcolor=True)}", end="")

    OK: str = f"{Color(g=255,bcolor=True)}"

    @staticmethod
    def fOK() -> None:
        """Sets the text color to GREEN"""
        print(f"{Color(g=255,bcolor=True)}", end="")

    CYAN: str = f"{Color(g=255,b=255,bcolor=True)}"

    @staticmethod
    def fCYAN() -> None:
        """Sets the text color to CYAN"""
        print(f"{Color(g=255,b=255,bcolor=True)}", end="")

    WOOD: str = f"{Color(120,81,45,bcolor=True)}\033[46m\033[7m"

    @staticmethod
    def fWOOD() -> None:
        """Sets the text color to CYAN, and the background to a WOODen color"""
        print(f"{Color(120,81,45,bcolor=True)}\033[46m\033[7m", end="")

    REPLIT: str = f"{Color(161, 138, 26, True)}"

    @staticmethod
    def fREPLIT() -> None:
        """Sets the text color to 161,138,26 in RGB"""
        print(f"{Color(162, 138, 26, True)}")

    GREEN = OK
    fGREEN = fOK
    YELLOW = WARNING
    fYELLOW = fWARNING
    RED = FAIL
    fRED = fFAIL

    class bold:
        """
        Contains bold versions of the other color codes
        """

        BROWN: str = f"\033[1m{Color(205,127,50,bcolor=True)}"

        @staticmethod
        def fBROWN() -> None:
            """Sets the text color to BROWN"""
            print(f"\033[1m{Color(205,127,50,bcolor=True)}", end="")

        WARNING: str = f"\033[1m{Color(236,232,26,bcolor=True)}"

        @staticmethod
        def fWARNING() -> None:
            """Sets the text color to YELLOW"""
            print(f"\033[1m{Color(236,232,26,bcolor=True)}", end="")

        FAIL: str = f"\033[1m{Color(255,bcolor=True)}"

        @staticmethod
        def fFAIL() -> None:
            """Sets the text color to RED"""
            print(f"\033[1m{Color(255,bcolor=True)}", end="")

        OK: str = f"\033[1m{Color(g=255,bcolor=True)}"

        @staticmethod
        def fOK() -> None:
            """Sets the text color to GREEN"""
            print(f"\033[1m{Color(g=255,bcolor=True)}", end="")

        CYAN: str = f"\033[1m{Color(g=255,b=255,bcolor=True)}"

        @staticmethod
        def fCYAN() -> None:
            """Sets the text color to CYAN"""
            print(f"\033[1m{Color(g=255,b=255,bcolor=True)}", end="")

        WOOD: str = f"\033[1m{Color(120,81,45,bcolor=True)}\033[46m\033[7m"

        @staticmethod
        def fWOOD() -> None:
            """Sets the text color to CYAN, and the background to a WOODen color"""
            print(f"\033[1m{Color(120,81,45,bcolor=True)}\033[46m\033[7m", end="")

        WHITE: str = f"\033[1m{Color(255,255,255,bcolor=True)}"

        @staticmethod
        def fWHITE() -> None:
            """Sets the text color to WHITE"""
            print(f"\033[1m{Color(255,255,255,bcolor=True)}", end="")

        RWHITE: str = f"\033[0m\033[1m{Color(255,255,255,bcolor=True)}"

        @staticmethod
        def fRWHITE() -> None:
            """RESETs the text color, then sets it to WHITE"""
            print(f"\033[0m\033[1m{Color(255,255,255,bcolor=True)}", end="")

        REPLIT: str = f"\033[1m{Color(161, 138, 26, True)}"

        @staticmethod
        def fREPLIT() -> None:
            """Sets the text color to 161,138,26 in RGB"""
            print(f"\033[1m{Color(162, 138, 26, True)}")

        GREEN = OK
        fGREEN = fOK
        YELLOW = WARNING
        fYELLOW = fWARNING
        RED = FAIL
        fRED = fFAIL


replitCursor: str = f"{bcolors.REPLIT}{bcolors.RESET}"
replit_cursor = replitCursor

cast = TypeVar("cast")


def inputCast(prompt: str = "", cast: Type = str, badCastMessage: str = "") -> cast:  # type: ignore[type-var]
    """# Function: input
      Displays your `prompt`, supports casting by default, with handling!
    # Inputs:
      prompt: str - The prompt, defaults to ""
      cast: Type - The Type to cast the input to, defaults to str
      badCastMessage: str - The message to dispaly upon reciving input that can't be casted to `cast`, can be set to `"None"` to not have one, defaults to f"That is not a vaild {cast.__name__}, please try again."

    # Returns:
      cast - The user's input, casted to `cast`

    # Raises:
      None"""
    if not badCastMessage:
        badCastMessage = f"That is not a vaild {cast.__name__}, please try again."
    ret = ""
    abc = ""
    while ret == "":
        try:
            abc = input(prompt)
            cast(abc)
            ret = abc
            break
        except ValueError:
            if badCastMessage != "None":
                print(badCastMessage)
    return cast(ret)


def replitInput(prompt: str = "", cast: Type = str, badCastMessage: str = "") -> cast:  # type: ignore[type-var]
    """# Function: replitInput
      Displays your `prompt` with the replit cursor on the next line, supports casting by default, with handling!
    # Inputs:
      prompt: str - The prompt, defaults to ""
      cast: Type - The Type to cast the input to, defaults to str
      badCastMessage: str - The message to dispaly upon reciving input that can't be casted to `cast`, can be set to "No message" to not have one, defaults to f"That is not a vaild {cast.__name__}, please try again."

    # Returns:
      cast - The user's input, casted to `cast`

    # Raises:
      None"""
    if prompt:
        print(prompt)
    return inputCast(f"{replitCursor} ", cast, badCastMessage)


replit_input = replitInput


def cprint(text: str = "") -> None:
    """# Function: cprint
      Displays your `text` in a random color (from bcolors).
    # Inputs:
      text: str - The text to color, defaults to ""

    # Returns:
      None

    # Raises:
      None"""
    colordict = {
        "GREEN": bcolors.GREEN,
        "RED": bcolors.RED,
        "YELLOW": bcolors.YELLOW,
        "CYAN": bcolors.CYAN,
        "REPLIT": bcolors.REPLIT,
        "BROWN": bcolors.BROWN,
        "WHITE": bcolors.WHITE,
    }
    colornames = ["GREEN", "RED", "YELLOW", "CYAN", "REPLIT", "BROWN", "WHITE"]
    color = colordict[robj(colornames)]
    print(f"{color}{text}")


class ProgramWarnings(UserWarning):
    """Warnings Raised for user defined Warnings in `console.warn` by default."""


class AssertationWarning(UserWarning):
    """Warnings Raised for assertion errors in `console.assert_()`."""


class console:
    """Limited Functionality version of JavaScript's console functions"""

    __counters__: dict = {"default": 0}
    __warnings__: List[str] = []

    @alias(print)
    @staticmethod
    def log(*args, **kwargs) -> None:
        """print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

        Prints the values to a stream, or to sys.stdout by default.
        Optional keyword arguments:
        file:  a file-like object (stream); defaults to the current sys.stdout.
        sep:   string inserted between values, default a space.
        end:   string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream."""
        print(*args, **kwargs)

    @alias(print)
    @staticmethod
    def info(*args, **kwargs) -> None:
        """print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

        Prints the values to a stream, or to sys.stdout by default.
        Optional keyword arguments:
        file:  a file-like object (stream); defaults to the current sys.stdout.
        sep:   string inserted between values, default a space.
        end:   string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream."""
        print(*args, **kwargs)

    @alias(print)
    @staticmethod
    def debug(*args, **kwargs) -> None:
        """print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

        Prints the values to a stream, or to sys.stdout by default.
        Optional keyword arguments:
        file:  a file-like object (stream); defaults to the current sys.stdout.
        sep:   string inserted between values, default a space.
        end:   string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream."""
        print(*args, **kwargs)

    @staticmethod
    def warn(warning: Any, class_: Optional[Type[Warning]] = ProgramWarnings) -> None:
        """# Function: console.warn
          Issue a warning
        # Inputs:
          warning: Any - The variable to use as a warning
          class_: class - The class to raise the warning from, defaults to ProgramWarnings

        # Returns:
          None

        # Raises:
          None"""
        ind = 1
        warn = warning
        while warn in console.__warnings__:
            warn = f"{warning}({ind})"
            ind += 1
        console.__warnings__.append(warn)
        ww(warn, class_, 2)

    @staticmethod
    def error(*args, **kwargs) -> None:
        """print(value, ..., sep=' ', end='\n', file=sys.stderr, flush=False)

        Prints the values to sys.stderr.
        Optional keyword arguments:
        sep:   string inserted between values, default a space.
        end:   string appended after the last value, default a newline.
        flush: whether to forcibly flush the stream."""
        print(bcolors.FAIL, *args, bcolors.RESET, file=sys.stderr, **kwargs)

    @staticmethod
    def assert_(condition: bool, message: str = "Assertion Failed") -> None:
        """# Function: console.assert_
          Makes an assertion check
        # Inputs:
          condition: bool - The condition to run an assert check on
          message: str - The message to raise if the assertion is False, defaults to "Assertion Failed"

        # Returns:
          None

        # Raises:
          None"""
        if not condition:
            console.warn(message, AssertationWarning)

    @staticmethod
    def count(label: str = "default") -> None:
        """# Function: console.count
          Increment a counter by one
        # Inputs:
          label: str - The counter to increment, defaults to "default"

        # Returns:
          None

        # Raises:
          None"""
        if console.__counters__[label]:
            console.__counters__[label] += 1
        else:
            console.__counters__[label] = 1
        print(f"{label}: {console.__counters__[label]}")

    @staticmethod
    def countReset(label: str = "default") -> None:
        """# Function: console.countReset
          Reset a counter to 0
        # Inputs:
          label: str - The counter to reset, defaults to "default"

        # Returns:
          None

        # Raises:
          None"""
        console.__counters__[label] = 0

    @alias(clear)
    @staticmethod
    def clear(ascii: bool = False) -> None:
        """# Function: console.clear
          Clears the screen
        # Inputs:
          ascii: bool - Wether to use ASCII to clear the screen, defaults to False

        # Returns:
          None

        # Raises:
          None"""
        clear(ascii)


sql: Type = fql.sql


def removePrefix(text: str, prefix: str) -> str:
    """# Function: removePrefix
    If `prefix` is at the beginning of `text`, return `text` without `prefix`, otherwise return `text`
    # Inputs:
      text: str - The text to remove the prefix from
      prefix: str - The prefix to remove from the text

    # Returns:
      str - `text` without `prefix`

    # Raises:
      None"""
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


remove_prefix = removePrefix


def removeSuffix(text: str, suffix: str) -> str:
    """# Function: removeSuffix
    If `suffix` is at the end of `text`, return `text` without `suffix`, otherwise return `text`
    # Inputs:
      text: str - The text to remove the suffix from
      suffix: str - The suffix to remove from the text

    # Returns:
      str - `text` without `suffix`

    # Raises:
      None"""
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


remove_suffix = removeSuffix


def isMath(equation: str) -> bool:
    """# Function: isMath
    Checks whether a given `equation` is actually an equation or not
    Function provided by @python660 on Replit Ask
    # Inputs:
      equation: str - The string to check to see if it is an equation

    # Returns:
      bool - Whether the given equation is a math problem

    # Raises:
      None"""
    return all([True if char in "1234567890*/+-.^%!" else False for char in equation])


def makeError(
    name: str, message: object, module: str = "builtins", raise_: bool = True
) -> Union[NoReturn, object]:
    """# Function: isMath
    Makes a custom error using the provided parts
    # Inputs:
      name: str - The name of the error
      message: object - The error content
      module: str - The module to say the error came from, defaults to "builtins"
      raise_: bool - Wether to raise the error or return it, defaults to rasing

    # Returns:
      Union[NoReturn, object] - Raises an error (NoReturn) or returns the error

    # Raises:
      If raises_, then User Provided Error, else None"""
    if raise_:
        raise type(name, (Exception,), {"__module__": module, "__name__": name})(
            message
        )
    else:
        return type(name, (Exception,), {"__module__": module, "__name__": name})(
            message
        )


class cur:
    """Contains functions to hide and show the cursor"""

    @staticmethod
    def hide() -> None:
        """# Function: cur.hide
        Hides the cursor
        # Inputs:
        None

        # Returns:
        None

        # Raises:
        None"""
        flushPrint("\033[?25l")

    @staticmethod
    def show() -> None:
        """# Function: cur.show
        Shows the cursor
        # Inputs:
        None

        # Returns:
        None

        # Raises:
        None"""
        flushPrint("\033[?25h")


def hidden(func):
    """# Function: hidden
    A wrapper that hides the cursor
    # Inputs:
    function

    # Returns:
    wrapper

    # Raises:
    None"""

    def wrapper(*args, **kwargs):
        cur.hide()
        try:
            out = func(*args, **kwargs)  # type: ignore
        except Exception as E:
            cur.show()
            raise E
        cur.show()
        return out

    return wrapper


def menu(options: dict, title: str = "") -> object:
    raise NotImplementedOnWindowsException(
        "This method is not implemented for Windows machines"
    )


if fkey:

    @hidden
    def menu(options: dict, title: str = "") -> object:
        """# Function: menu
        Uses a nice interactive for the provided options
        # Inputs:
        options: dict - A dictionary of options and their return values

        # Returns:
        object - The user's selected option

        # Raises:
        None"""
        if type(options) != dict:
            raise ValueError(f"options must be a dictionary (passed a {type(options)})")
        if len(options) <= 1:
            raise ValueError(
                f"options must contain at least two choices (passed {len(options)})"
            )
        choices = list(options)
        limit = len(choices)
        current = 0
        selected = False
        UP = [fkey.KEYS["UP"], b"w", b"a", fkey.KEYS["LEFT"]]
        DOWN = [fkey.KEYS["DOWN"], b"s", b"d", fkey.KEYS["RIGHT"]]
        indicatorSize = len(str(limit)) * 2 + 1
        indicatorOffset = 999
        match indicatorSize:
            case 3:  # 1-9 options (Ten rolls over)
                indicatorOffset = 1
            case 5:  # 10-99 options (One Hundered rolls over)
                indicatorOffset = 0
            case 7:  # 100-999 options (One Thousand rolls over)
                indicatorOffset = -1
            case 9:  # 1000-9999 options (Ten Thousand rolls over)
                indicatorOffset = -2
            case 11:  # 10000-99999 options (One Hundred Thousand rolls over)
                indicatorOffset = -3
            case 13:  # 100000-999999 options (One Million rolls over)
                indicatorOffset = -4
            case 15:  # 1000000-9999999 options (Ten Million rolls over)
                indicatorOffset = -5
            case 17:  # 10000000-99999999 options (One Hundred Million rolls over)
                indicatorOffset = -6
            case 19:  # 100000000-999999999 options (One Billion rolls over)
                indicatorOffset = -7
            case (
                21
            ):  # 1000000000-9999999999 options (Ten Billion rolls over) (This exceeds integer limits, so if we get over this I've got no clue how.)
                indicatorOffset = -8
            case _:
                raise ValueError(
                    f"You have more menu options than was ever expected to be used, please notify the package author to add a offset mappting for an indicator size of {indicatorSize}."
                )
        menuWidth = max(
            [max([len(choice) for choice in choices]) + 4, indicatorSize * 2 + 7]
        )
        while not selected:
            clear()
            flushPrint(
                (title + "\n" if title else "")
                + f"╔{'═'*menuWidth}╗\n"
                + f"║  {f'{current+1}'}{' '*(len(str(limit))-len(str(current+1)))}/{limit}{' '*int(menuWidth/2-indicatorSize-2.5)}↑{' '*int((menuWidth-indicatorSize)/2-indicatorOffset+(1 if menuWidth%2==0 else 0))}  ║\n"
                + f"║←{' '*int(((menuWidth-len(choices[current]))/2)-1)}{choices[current]}{' '*int((menuWidth-len(choices[current]))/2-.5)}→║\n"
                + f"║{' '*int((menuWidth-1)/2)}↓{' '*int((menuWidth-1)/2+.5)}║\n"
                + f"╚{'═'*menuWidth}╝\n"
            )
            key = fkey.get(bytes=True, osReader=True)
            if key in UP:
                current -= 1
            elif key in DOWN:
                current += 1
            elif key in [fkey.KEYS["ENTER"]]:
                break
            if current > limit - 1:
                current = 0
            if current < 0:
                current = limit - 1
        return options[choices[current]]


def getRandomNumber() -> int:
    """# Function: getRandomNumber
    Returns 4
    # Inputs:
    None

    # Returns:
    int - 4

    # Raises:
    None"""
    return 4  # chosen by fair dice roll.
    # garunteed to be random.
