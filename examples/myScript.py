from ydotoolUtils.ydotool import wait, type_

from totoBotKey.parser import BaseScript
from totoBotKey.decorators import on


class MyScript(BaseScript):
    @on("+a")
    @staticmethod
    def doSmth():
        type_("Ctrl+A got hit")

    @on("p", "o")
    @staticmethod
    def doSmth2():
        type_("Shift + A got hit")
        wait(1000)
        type_("One second has passed")

    @staticmethod
    def init():
        print("innit")
