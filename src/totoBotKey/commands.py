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


def pressKeys(keys: str | list):
    l = list()
    for s in ["1", "0"]:
        for k in keys:
            l.append(f"{k}:{s}")
    key(l)


def clickAt(btn:Button, x:int, y:int):
    mousemove(x, y)
    click(btn)