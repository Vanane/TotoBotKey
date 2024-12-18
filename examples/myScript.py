"""_summary_
"""

from ydotoolUtils.ydotool import wait, type_

from totoBotKey.parser import BaseScript
from totoBotKey.decorators import on


class MyScript(BaseScript):
    """_summary_"""

    @on("^a")
    @staticmethod
    def doSmth():
        """_summary_"""
        type_("Ctrl+A got hit")

    @on("!a")
    @staticmethod
    def doSmth2():
        """_summary_"""
        type_("Shift + A got hit")
        wait(1000)
        type_("One second has passed")

    @staticmethod
    def init():
        print("innit")
