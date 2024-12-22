from ydotoolUtils.ydotool import wait, type_, click
from totoBotKey.parser import BaseScript
import totoBotKey.inputs as inputs
from totoBotKey.decorators import on, BindTypes
import ydotoolUtils.keys as keys


class MyScript(BaseScript):
    @on("+a")
    @staticmethod
    def doSmth():
        type_("Shift+A got hit")

    @on("a", bType=BindTypes.ANY)
    @staticmethod
    def doSmth4():
        type_("A got hit")

    @on("p", "o")
    @staticmethod
    def doSmth2():
        wait(1000)
        print("One second has passed")

    @on("BtnSide", bType=BindTypes.ANY)
    @staticmethod
    def doSmth3():
        while inputs.isPressed(keys.BTN_SIDE):
            click("BtnLeft")
            # wait(15)

    @on("BtnExtra")
    @staticmethod
    def doSmth4():
        print("prout")
        pass



    @staticmethod
    def init():
        print("innit")

