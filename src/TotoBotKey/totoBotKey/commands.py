"""Additional commands wrapping Ydotool calls"""

import time
from contextlib import contextmanager
from .commandsraw import click, key, mousemove, type_

from ydotoolUtils import ydotool
from .keys import Key
from .buttons import Button


def keydown(keys: int | list[int]):
    if not isinstance(keys, list):
        keys = [keys]

    key([f"{k}:1" for k in keys])

def keyup(keys: int | list[int]):
    if not isinstance(keys, list):
        keys = [keys]

    key([f"{k}:0" for k in keys])

def wait(ms):
    """Waits for a given time, in milliseconds.
    On a technical point, it pauses the execution thread.

    Args:
        ms (int): Time to wait, in milliseconds
    """
    time.sleep(int(ms) / 1000)


def pressKeys(keys: int | list[int]):
    """
    Operates all keydowns, then all keyups, for a given key or list of keys.
    
    Args:
    keys (int|list[int]): A keycode, or a list of keycodes, to press
    """
    if not isinstance(keys, list):
        keys = [keys]

    keydown(keys)
    keyup([reversed(keys)])


def clickAt(btn:Button, x:int, y:int):
    """
    Operates a mousemove(x, y), then a click(btn), in absolute position, the origin being the topmost-leftest corner
    
    Args:
    btn (totoBotKey.enums.Button): Button to press
    x (int): Absolute X position on the viewport
    y (int): Absolute Y position on the viewport
    """
    mousemove(x, y)
    click(btn)


@contextmanager
def holding(keys: int | list[int]):
    """Do smth like that : with holding(keys...):"""
    keydown(keys)
    try:
        yield
    finally:
        keyup(keys)
