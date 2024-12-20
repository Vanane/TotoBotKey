from ydotoolUtils.ydotool import wait, type_, click
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
        while inputs.isPressed(keys.Keys.BTN_("SIDE")):
            click("BtnLeft")
            wait(15)
  
    @staticmethod
    def init():
        print("innit")
