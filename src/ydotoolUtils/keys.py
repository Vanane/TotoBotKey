"""_summary_
"""

import os
from typing import Self


class Keys:
    """_summary_

    Returns:
        _type_: _description_
    """

    dumpFile = "./input-event-codes.h"
    keys: dict
    instance: object

    @staticmethod
    def getInstance() -> Self:
        """Returns the singleton's instance"""
        if not getattr(Keys, "instance", False):
            Keys.instance = Keys()
        return Keys.instance

    def __init__(self):
        if not os.path.exists(self.dumpFile):
            self.dumpKeys()

        self.registerKeys()
        Keys.instance = self

    def dumpKeys(self):
        """Creates a cleaned local copy of the file located at 
    `/usr/include/linux/input-event-codes.h`, for later use."""
        print(
            f"Extracting keyCodes from `/usr/include/linux/input-event-codes.h` into `{self.dumpFile}`"
        )

        os.system(
            f"cat /usr/include/linux/input-event-codes.h | gcc -dM -E - > {self.dumpFile}"
        )

    def registerKeys(self):
        """Reads the file created by dumpKeys() to instantiate a dictionary
        of all keycodes that can be read and/or called in TotoBotKey.
        """
        self.keys = dict()
        with open(self.dumpFile, encoding="utf-8") as f:
            while l := f.readline().split():
                try:
                    self.keys[l[1]] = l[2]
                    setattr(Keys, l[1], l[2])
                except Exception:
                    pass

    @staticmethod
    def KEY_(k: str) -> int:
        """Returns the keycode representing the given key name"""
        return getattr(Keys, f"KEY_{k}")

    @staticmethod
    def BTN_(b: str) -> int:
        """Returns the keycode representing the given mouse button name"""
        return getattr(Keys, f"BTN_{b}")
