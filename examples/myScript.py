from ydotoolUtils.ydotool import wait, type_, click, pressKeys
from totoBotKey.parser import BaseScript
import totoBotKey.inputs as inputs
from totoBotKey.decorators import on
import ydotoolUtils.keys as keys


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

    @on("BtnSide")
    @staticmethod
    def doSmth3():
        while inputs.isPressed(keys.BTN_SIDE):
            click("BtnLeft")
            # wait(15)

    @on("^i")
    @staticmethod
    def autoIndentAll():
        for i in range(12):
            MyScript.autoIndent()

    @staticmethod
    def autoIndent():
        pressKeys([keys.KEY_LEFTCTRL, keys.KEY_LEFTSHIFT, keys.KEY_I])
        wait(250)
        pressKeys([keys.KEY_LEFTCTRL, keys.KEY_S])
        wait(250)
        pressKeys([keys.KEY_LEFTCTRL, keys.KEY_Z])
        wait(250)

    @staticmethod
    def init():
        print("innit")
