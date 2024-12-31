"""Static parser that will load a python script and run various
analysis to deem it TotoBotKey-able."""

import importlib
from types import ModuleType
from . import keys


class BaseScript:
    """Class to inherit any script from"""

    @staticmethod
    def init():
        """Main script that will be called at the beginning."""


class ParserResult:
    """Data resulting from the parser"""

    pythonClass: BaseScript
    errors: list
    isAsync: bool

    def __init__(self, p, e, a):
        self.pythonClass = p
        self.errors = e
        self.isAsync = a


errors: list


def init():
    global errors
    errors = list()


def getErrors() -> list | None:
    """Returns the list of potential errors while parsing the script,
    or None if there's none."""
    if hasErrors():
        return errors
    return None


def addError(msg: str):
    """Adds an errors to the parser, when parsing a script."""
    global errors
    if not errors:
        errors = list()
    errors.append(msg)


def hasErrors() -> bool:
    """Tells whether the parsing led to errors or not."""
    if errors is None:
        return False
    return bool(len(errors))


def parseScript(script: str) -> ParserResult | bool:
    """Determines whether a given python script contains a script that can be potentially
    run by TotoBotKey.

    Args:
        script (str): The script to parse

    Returns:
        If the script can be run, it will return a result, with potential errors to look into.
        If not, returns False.

    """
    mod = importlib.import_module(script)
    clss = getScriptClassReflect(mod)
    if clss is None:
        print("No script found.")
        return False

    print(f"Script found : {clss.__name__}")

    return ParserResult(clss, getErrors(), False)


def parseEventDecorator(*binds) -> tuple[list, list]:
    """Tries to convert a humanish-readable event binder into a keycode combination.
    See README.md for a list of allowed decorator syntaxes.

    Args:
        bind (str): The string to parse

    Returns:
        tuple[list, list]: The resulting characters and modifiers that were parsed,
        respectively.
    """
    modsDict = {
        "^": keys.KEY_("LEFTCTRL"),
        "+": keys.KEY_("LEFTSHIFT"),
        "!": keys.KEY_("LEFTALT"),
        "#": keys.KEY_("MENU"),
    }
    keysDict = {
        "btnleft": keys.BTN_("LEFT"),
        "btnright": keys.BTN_("RIGHT"),
        "btnwheel": keys.BTN_("WHEEL"),
        "btn4": keys.BTN_("4"),
        "btn5": keys.BTN_("5"),
        "btnside": keys.BTN_("SIDE"),
        "btnextra": keys.BTN_("EXTRA"),
    }

    mods = set()
    chars = set()

    for bind in binds:
        bind = str(bind).lower()
        i = 0
        while i < len(bind):
            l = bind[i]
            if modsDict.get(l, False):
                mods.add(int(modsDict[l]))
            else:
                t = ""
                for j in range(len(bind[i:])):
                    k = bind[i + j]
                    if k.isalnum():
                        t += k
                    if not k.isalnum() or len(bind[i:]) == j + 1:
                        key = f"KEY_{t.upper()}"
                        try:
                            keycode = keysDict.get(t, keys.get(key))
                            if keycode is not None:
                                chars.add(int(keycode))
                            else:
                                raise KeyError
                        except KeyError:
                            addError(
                                f"Error : Key '{key}' or keyword '{t}' not found when trying to parse expression '{bind}'."
                            )
                        i += j
                        break
            i += 1

    return (sorted(chars), sorted(mods))


def getScriptClassReflect(mod: ModuleType) -> type | None:
    """Returns the type that corresponds to the first class inheriting from BaseScript
    find in a given module.

    Returns:
        type | None: The type of the class inheriting baseScript if found, else None.
    """
    for i in mod.__dict__:
        attr: type = getattr(mod, i)
        if isinstance(attr, type) and BaseScript in attr.__bases__:
            return attr
    return None
