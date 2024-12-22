import os


DUMP_FILE = "./input-event-codes.h"
keysDict: dict


def init():
    if not os.path.exists(DUMP_FILE):
        dumpKeys()

    readFromDump()


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


def readFromDump():
    """Reads the file created by dumpKeys() to instantiate a dictionary
    of all keycodes that can be read and/or called in TotoBotKey.
    """
    global keysDict
    keysDict = dict()

    with open(DUMP_FILE, encoding="utf-8") as f:
        while l := f.readline().split():
            try:
                keysDict[l[1]] = int(l[2], 0)
                globals()[l[1]] = int(l[2], 0)
            except Exception:
                pass


def get(keyName: str):
    """Return the keycode representing the given key name, e.g. EV_KEY, SYN_BTN, etc."""
    return globals().get(keyName, None)


def KEY_(k: str) -> int:
    """Returns the keycode representing the given key name"""
    return int(globals()[f"KEY_{k.upper()}"])


def BTN_(b: str) -> int:
    """Returns the keycode representing the given mouse button name"""
    return int(globals()[f"BTN_{b.upper()}"])
