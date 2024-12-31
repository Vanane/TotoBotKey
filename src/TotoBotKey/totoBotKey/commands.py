"""Available commands list"""

import time
from ydotoolUtils import ydotool
from .enums import Button, Key

def click(btn:Button):
    """Calls ydotool to simulate a click at the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    ydotool.click(format(Button.press(btn), "x"))


def mousemove(x: int, y: int):
    """Calls ydotool to simulate a mouse movement from its current point, to the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    ydotool.mousemove(x, y)



def type_(text: str):
    """Calls ydotool to simulate a text being typed

    Args:
        text (str): Text to type
    """
    ydotool.type_(text)

def key(keys: str | list):
    """Calls ydotool to simulate keystrokes

    Args:
        keys (str): Keys to strike all at once
    """
    ydotool.key(keys)


"""
Ydotool native functions
"""

def wait(ms):
    """Waits for a given time, in milliseconds.

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
