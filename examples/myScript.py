from totoBotKey.parser import BaseScript
from totoBotKey import inputs
from totoBotKey.decorators import on, BindType
from totoBotKey.enums import Key, Button
from totoBotKey.commands import type_, click, wait, clickAt

class MyScript(BaseScript):
    @on("+a")
    @staticmethod
    def onShiftA():
        """SExample : macro to type some text when specifically Shift+A is pressed"""
        type_("Shift+A got hit")

    @on("a", bType=BindType.ANY)
    @staticmethod
    def onAnyA():
        """Example : macro to type some text whenever A is pressed in any situation"""        
        type_("A got hit")

    @on("p", "o")
    @staticmethod
    def onAnyPO():
        """Example : macro binded on several non-mod keys"""
        wait(1000)
        print("One second has passed")

    @on("BtnSide", bType=BindType.ANY)
    @staticmethod
    def spamClick():
        """Example : concrete example of a macro to spamclick the left button, while one of the extra buttons is held down"""
        while inputs.isPressed(Key.BTN_SIDE):
            click(Button.BtnLeft)

    @staticmethod
    def init():
        print("innit")

