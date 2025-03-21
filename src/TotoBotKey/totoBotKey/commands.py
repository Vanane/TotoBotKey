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
    l1 = list()
    l0 = list()
    if not isinstance(keys, list):
        keys = [keys]
    s = "1"
    for k in keys:
        l1.append(f"{k}:{s}")
    s = "0"
    for k in keys:
        l0.append(f"{k}:{s}")
    l0.reverse()
    key(l1 + l0)


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
