"""decorators
"""

from enum import Enum
from . import inputs
from . import parser


class BindTypes(Enum):
    ANY = 1
    """The binding will trigger without regard for any other key states but the binding"""
    ONLY = 2
    """The binding will trigger if those keys are the only keys pressed currently"""


def on(*bind, bType:BindTypes = BindTypes.ONLY):
    """
    Binds a function to a particular combination of keypresses, with a naturalish syntax.
    Some keys can't be used through this decorator, such as Delete, Insert, F1-12, etc.
    Example :
        "^+!#a" : Ctrl + Shift + Alt + Super/Win/Menu + A Key
    """
    def d(f):
        match bType:
            case BindTypes.ANY:
                (chars, mods) = parser.parseEventDecorator(*bind)
                inputs.addEventOnAny(sorted(chars + mods), f)
            case BindTypes.ONLY:
                (chars, mods) = parser.parseEventDecorator(*bind)
                inputs.addEventOnOnly(sorted(chars + mods), f)
        return f
    return d


def onRaw(*bind):
    """
    Binds a function to a particular combination of keys given explicitely,
    bypassing the translation
    Example :
    >>> onRaw(KEY_LEFTCTRL, KEY_LEFTALT, KEY_DELETE) : Ctrl + Alt + Delete Key
    """
    def d(f):
        inputs.addEventOnOnly(sorted(bind), f)
        return f
    return d
