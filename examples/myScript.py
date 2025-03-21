from totoBotKey.parser import BaseScript
from totoBotKey.inputs import isPressed
from totoBotKey.decorators import on, BindType, script
from totoBotKey.commands import wait, clickAt, pressKeys
from totoBotKey.keys import Key
from totoBotKey.buttons import Button
from totoBotKey.commandsraw import type_, key, mousemove, click


class MyScript(BaseScript):
    @on("+a")
    @staticmethod
    def onShiftA():
        """Example : macro to type some text when specifically Shift+A is pressed"""
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
        while isPressed(Button.EXTRA):
            click(Button.LEFT)

    @on("+t")
    @staticmethod
    def test():
        wait(500)
        clickAt(Button.LEFT, 800, 400)
        wait(500)
        pressKeys([Key.A, Key.B])
        wait(500)
        pressKeys(Key.C)
        wait(500)

    @staticmethod
    def init():
        print("innit")
