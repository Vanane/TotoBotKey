from ydotoolUtils.ydotool import wait, type_, click, pressKeys
from totoBotKey.parser import BaseScript
import totoBotKey.inputs as inputs
from totoBotKey.decorators import on, onOnly
import ydotoolUtils.keys as keys


class MyScript(BaseScript):
    @onOnly("+a")
    @staticmethod
    def doSmth():
        type_("Ctrl+A got hit")

    @onOnly("p", "o")
    @staticmethod
    def doSmth2():
        type_("Shift + A got hit")
        wait(1000)
        type_("One second has passed")

    @onOnly("BtnSide")
    @staticmethod
    def doSmth3():
        while inputs.isPressed(keys.BTN_SIDE):
            click("BtnLeft")
            # wait(15)

    @onOnly("BtnExtra")
    @staticmethod
    def doSmth4():
        print("prout")
        pass



    @staticmethod
    def init():
        print("innit")
