from totoBotKey.parser import BaseScript
from totoBotKey.inputs import isPressed
from totoBotKey.decorators import on, BindType
from totoBotKey.enums import Key, Button
from totoBotKey.commands import type_, click, wait, clickAt, pressKeys

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
        while isPressed(Key.BTN_SIDE):
            click(Button.BtnLeft)

    @on("+t")
    @staticmethod
    def test():
        wait(500)
        clickAt(Button.BtnLeft, 800, 400)
        wait(500)
        pressKeys([Key.KEY_A, Key.KEY_B])
        wait(500)
        pressKeys(Key.KEY_C)
        wait(500)

    @staticmethod
    def init():
        print("innit")

