"""Ydotool native functions"""

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

def key(keys: Key | list[Key]):
    """Calls ydotool to simulate keystrokes

    Args:
        keys (str): Keys to strike all at once
    """
    ydotool.key(keys)
