"""decorators
"""

import totoBotKey.inputs as inputs
from . import parser


def on(*bind):
    """
    Binds a function to a particular combination of keypresses, with a naturalish syntax.
    Some keys can't be used through this decorator, such as Delete, Insert, F1-12, etc.
    Example :
        "^+!#a" : Ctrl + Shift + Alt + Super/Win/Menu + A Key
    """
    def d(f):
        (chars, mods) = parser.parseEventDecorator(*bind)
        keys = list(map(str, sorted(mods + chars)))
        inputs.addEventOnAny("+".join(keys), f)
        return f

    return d

def onAny(*bind):
    return on(bind)

def onOnly(*bind):
    """
    Binds a function to a particular combination of keypresses, calling it only when this combination and nothing else is pressed.
    Example :
    >>> on("a")     # Triggers whenever A is pressed, along with other keys.
    >>> onOnly("a") # Triggers whenever A and only A is pressed. "Ctrl+A" or "Shift+A" among others, won't trigger it.
    """

    def d(f):
        (chars, mods) = parser.parseEventDecorator(*bind)
        keys = list(map(str, sorted(mods + chars)))
        inputs.addEventOnAny("+".join(keys), f)
        return f
    return d


def onRaw(bind: str):
    """
    Binds a function to a particular combination of keys given explicitely,
    bypassing the translation
    Example :
        "KEY_LEFTCTRL+KEY_LEFTALT+KEY_DELETE" : Ctrl + Alt + Delete Key
    """

    def d(f):
        inputs.addEventOnAny("+".join(sorted(bind.split("+"))), f)
        return f

    return d
