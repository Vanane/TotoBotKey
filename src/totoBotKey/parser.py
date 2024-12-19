"""parser
"""

import importlib
from types import ModuleType
from ydotoolUtils import Keys


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


class Parser:
    """Static parser that will load a python script and run various
    analysis to deem it TotoBotKey-able."""

    @staticmethod
    def getErrors() -> list | None:
        """Returns the list of potential errors while parsing the script,
        or None if there's none."""
        if Parser.hasErrors():
            return Parser.errors
        return None

    @staticmethod
    def addError(msg: str):
        """Adds an errors to the parser, when parsing a script."""
        if not hasattr(Parser, "errors"):
            Parser.errors = list()
        Parser.errors.append(msg)

    @staticmethod
    def hasErrors() -> bool:
        """Tells whether the parsing led to errors or not."""
        return hasattr(Parser, "errors")

    @staticmethod
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
        clss = Parser.getScriptClassReflect(mod)
        if clss is None:
            print("No script found.")
            return False

        print(f"Script found : {clss.__name__}")

        return ParserResult(clss, Parser.getErrors(), False)

    @staticmethod
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
            "^": Keys.KEY_("LEFTCTRL"),
            "+": Keys.KEY_("LEFTSHIFT"),
            "!": Keys.KEY_("LEFTALT"),
            "#": Keys.KEY_("MENU"),
        }
        keysDict = {
            "btnleft": Keys.BTN_("LEFT"),
            "btnright": Keys.BTN_("RIGHT"),
            "btnwheel": Keys.BTN_("WHEEL"),
            "btn4": Keys.BTN_("4"),
            "btn5": Keys.BTN_("5"),
        }

        mods = set()
        chars = set()

        for bind in binds:
            print(bind[0])
            bind = str(bind).lower()
            i = 0
            while i < len(bind):
                l = bind[i]
                if modsDict.get(l, False):
                    mods.add(modsDict[l])
                else:
                    t = ""
                    for j in range(len(bind[i:])):
                        k = bind[i + j]
                        if k.isalnum():
                            t += k
                        if not k.isalnum() or len(bind[i:]) == j + 1:
                            key = f"KEY_{t.upper()}"
                            try:
                                chars.add(keysDict.get(t, getattr(Keys, key)))
                            except AttributeError:
                                Parser.addError(
                                    f"Error : Key '{key}' not found when trying to parse expression '{bind}'."
                                )
                            i += j
                            break
                i += 1

        return (sorted(chars), sorted(mods))

    @staticmethod
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
