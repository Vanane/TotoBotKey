"""ydotool
"""

import os
import time

from ydotoolUtils.enums import CLICK_BTN_CODES

"""
Ydotool native functions
"""


def click(btn=None):
    """Calls ydotool to simulate a click at the given coordinates

    Args:
        x (int): Position X on the viewport
        y (int): Position Y on the viewport
    """
    if not btn in CLICK_BTN_CODES:
        raise ValueError(f"Mouse button '{btn}' not in {list(CLICK_BTN_CODES.keys())}")
    print(CLICK_BTN_CODES[btn])
    os.system(f"ydotool click {CLICK_BTN_CODES[btn]}")


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


def key(keys: str):
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
