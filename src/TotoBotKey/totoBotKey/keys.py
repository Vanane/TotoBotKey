import os

from .enums import Key


DUMP_FILE = "./input-event-codes.h"
keysDict: dict


def init():
    if not os.path.exists(DUMP_FILE):
        dumpKeys()

    readFromDump(Key)


def dumpKeys():
    """Creates a cleaned local copy of the file located at
    `/usr/include/linux/input-event-codes.h`, for later use."""
    if not os.path.exists(DUMP_FILE):
        print(
            f"Extracting keyCodes from `/usr/include/linux/input-event-codes.h` into `{DUMP_FILE}`"
        )
        os.system(
            f"cat /usr/include/linux/input-event-codes.h | gcc -dM -E - > {DUMP_FILE}"
        )


def readFromDump(dump:object):
    """Reads the file created by dumpKeys() to instantiate a dictionary
    of all keycodes that can be read and/or called in TotoBotKey.

    dump(object): Object that will receive the dumped keycodes, as its own attributes
    """
    global keysDict
    keysDict = dict()

    with open(DUMP_FILE, encoding="utf-8") as f:
        while l := f.readline().split():
            try:
                keysDict[l[1]] = int(l[2], 0)

                setattr(dump, l[1], int(l[2], 0))
            except Exception:
                pass


def get(keyName: str):
    """Return the keycode representing the given key name, e.g. EV_KEY, SYN_BTN, etc."""
    return getattr(Key, keyName, None)


def KEY_(k: str) -> int:
    """Returns the keycode representing the given key name"""
    return int(get(f"KEY_{k.upper()}"))


def BTN_(b: str) -> int:
    """Returns the keycode representing the given mouse button name"""
    return int(get(f"BTN_{b.upper()}"))
