from .parser import *
from .input import *


def on(bind):
    '''
    Binds a function to a particular combination of keypresses, with a naturalish syntax.
    Some keys can't be used through this decorator, such as Delete, Insert, F1-12, etc.
    Example :
        "^+!#a" : Ctrl + Shift + Alt + Super/Win/Menu + A Key
    '''
    def d(f):
        (chars, mods) = Parser.parseEventDecorator(bind)
        keys = sorted(mods + chars)
        InputManager.addEvent("+".join(keys), f)        
        return f
    return d


def onExplicit(bind:str):
    '''
    Binds a function to a particular combination of keys given explicitely, bypassing the translation
    Example :
        "KEY_LEFTCTRL+KEY_LEFTALT+KEY_DELETE" : Ctrl + Alt + Delete Key
    '''
    def d(f):
        InputManager.addEvent(bind, f)
        return f
    return d
