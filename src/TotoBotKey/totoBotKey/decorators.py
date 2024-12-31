"""decorators
"""

from enum import Enum
from . import inputs
from . import parser


class BindType(Enum):
    ANY = 1
    """This binding will be triggered whenever all of its keys, among others, are pressed"""
    ONLY = 2
    """This binding will be triggered only when all of its key and nothing else are pressed"""


def on(*bind, bType:BindType = BindType.ONLY):
    """
    Binds a function to a particular combination of keypresses, with a naturalish syntax.
    Some keys can't be used through this decorator, such as Delete, Insert, F1-12, etc.
    See syntax in Scripting.md.
    Examples :
    >>> on("a") : Called when A, and only A, is pressed
    >>> on("a", bType = BindType.ANY) : Called whenever A is pressed
    >>> on("+a") : Called when only 'Shift + A' are pressed
    >>> on("^a") : Called when only 'LeftCtrl + A' are pressed
    >>> on("!a") : Called when only 'LeftAlt + A' are pressed
    >>> on("#a") : Called when only 'Menu + A' are pressed
    >>> on("a", "b") : Called when only 'A + B' are pressed
    >>> on("+a", "b") : Called when only 'Shift + A + B' are pressed
    """
    def d(f):
        (chars, mods) = parser.parseEventDecorator(*bind)
        inputs.addEvent(sorted(chars + mods), f, True if bType == BindType.ONLY else False)
        return f
    return d


def onRaw(*bind, bType:BindType = BindType.ONLY):
    """
    Binds a function to a particular combination of keys given explicitely,
    bypassing the translation
    Example :
    >>> onRaw(KEY_LEFTCTRL, KEY_LEFTALT, KEY_DELETE) : Ctrl + Alt + Delete Key
    """
    def d(f):
        inputs.addEvent(sorted(bind), f, True if bType == BindType.ONLY else False)
        return f
    return d
