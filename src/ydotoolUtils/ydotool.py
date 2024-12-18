"""ydotool
"""

import os
import time

"""
Ydotool native functions
"""


def click(x: int, y: int):
    """Calls ydotool to simulate a click at the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    os.system(f"ydotool click {x} {y}")


def mousemove(x: int, y: int):
    """Calls ydotool to simulate a mouse movement from its current point, to the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    os.system(f"ydotool mousemove {x} {y}")


def type_(text: str):
    """Calls ydotool to simulate a text being typed

    Args:
        text (str): Text to type
    """
    os.system(f"ydotool type {text}")


def keyss(keys: str):
    """Calls ydotool to simulate keystrokes

    Args:
        keys (str): Keys to strike all at once
    """
    if type_(keys) is list:
        keys = " ".join(keys)
    os.system(f"ydotool key {keys}")


"""
Additionnal functions
"""


def wait(ms):
    """Waits for a given time, in milliseconds.

    Args:
        ms (int): Time to wait, in milliseconds
    """
    time.sleep(int(ms) / 1000)
