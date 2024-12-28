"""ydotool
"""

import os
import time


def _call(*args):
    c = f"ydotool {' '.join(list(map(str, args)))}"
    os.system(c)

def click(btn):
    """Calls ydotool to simulate a click at the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    _call("click", btn)


def mousemove(x: int, y: int, a=True):
    """Calls ydotool to simulate a mouse movement from its current point, to the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    
    # Workarounds for ydotool's broken mousemove command :
    # --absolute option doesn't work and will place the mouse at the top-left corner.
    # A workaround is to make two commands and use the relative option, from 0-0 coordinates
    # 
    # ydotool seems to multiply the coordinates by 2, so dividing arguments by 2 fixes it.
    if a:
        _call("mousemove", "-x", -8192, "-y", -8192)
    _call("mousemove", "-x", x / 2, "-y", y / 2)


def type_(text: str):
    """Calls ydotool to simulate a text being typed

    Args:
        text (str): Text to type
    """
    _call("type", text)


def key(keys: str | list):
    """Calls ydotool to simulate keystrokes

    Args:
        keys (str): Keys to strike all at once
    """
    if isinstance(keys, list):
        keys = " ".join(keys)
    _call("key",  keys)
