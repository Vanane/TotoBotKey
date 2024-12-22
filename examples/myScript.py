from totoBotKey.parser import BaseScript
from totoBotKey import inputs
from totoBotKey.decorators import on, BindType
from totoBotKey.enums import Key, Button
from totoBotKey.commands import type_, click, wait, clickAt

class MyScript(BaseScript):
    @on("+a")
    @staticmethod
    def doSmth():
        type_("Shift+A got hit")

    @on("a", bType=BindType.ANY)
    @staticmethod
    def doSmth4():
        type_("A got hit")

    @on("p", "o")
    @staticmethod
    def doSmth2():
        wait(1000)
        print("One second has passed")

    @on("BtnSide", bType=BindType.ANY)
    @staticmethod
    def doSmth3():        
        while inputs.isPressed(Key.BTN_SIDE):
            click(Button.BtnLeft)
            # wait(15)

    @on("BtnExtra", bType=BindType.ANY)
    @staticmethod
    def doSmth5():
        clickAt(Button.BtnLeft, 400, 400)


    @staticmethod
    def init():
        print("innit")

